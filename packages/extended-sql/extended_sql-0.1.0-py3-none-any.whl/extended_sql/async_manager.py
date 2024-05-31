import logging
from asyncio import current_task
from functools import partial
from typing import Any, AsyncIterator

from sqlalchemy import schema as alchemy_schema
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_scoped_session

from .models import ExtendedSQLModel
from .utils import create_async_engine, create_async_session_marker

_logger = logging.getLogger("extended_sql")


class AsyncDBManager:
    def __init__(
        self,
        uri: str,
        name: str = "engine",
        pool_size: int = 100,
        max_overflow: int = 0,
        pool_pre_ping: bool = False,
        echo: bool = False,
        expire_on_commit: bool = False,
        autocommit: bool = False,
        autoflush: bool = False,
        **kwargs,
    ):
        self.engine = create_async_engine(
            uri,
            name=name,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_pre_ping=pool_pre_ping,
            echo=echo,
            **kwargs,
        )
        self.session_maker = create_async_session_marker(
            engine=self.engine,
            expire_on_commit=expire_on_commit,
            autocommit=autocommit,
            autoflush=autoflush,
        )
        self.session = async_scoped_session(self.session_maker, scopefunc=current_task)

    def _check_engine(self) -> None:
        if self.engine is None:
            raise Exception("Engine is closed or not initialized.")

    def get_engine(self) -> AsyncEngine:
        """Return the engine if it is set up."""
        self._check_engine()
        return self.engine

    async def close(self):
        """Dispose of the engine."""
        self._check_engine()
        await self.engine.dispose()

    async def initialize(
        self,
        drop_: bool = True,
        model: ExtendedSQLModel = None,
        just_drop_: bool = False,
    ) -> None:
        """
        Initialize the database.

        :param drop_: Whether to drop the table.
        :type drop_: bool
        :param just_drop_: Whether to just drop the table.
        :type just_drop_: bool
        :param model: The model to initialize (if not provided will initialize all models)
        :type model: ExtendedSQLModel
        """
        _logger.debug(f"Initializing database with drop={drop_} and model={model}")
        async with self.get_engine().begin() as conn:
            if model is not None:
                if drop_ or just_drop_:
                    await conn.run_sync(partial(model.__table__.drop, checkfirst=True))
                if not just_drop_:
                    await conn.run_sync(
                        partial(model.__table__.create, checkfirst=True)
                    )
            else:
                if drop_ or just_drop_:
                    await conn.run_sync(ExtendedSQLModel.metadata.drop_all)
                if not just_drop_:
                    await conn.run_sync(ExtendedSQLModel.metadata.create_all)

    async def _get_session(self) -> AsyncIterator[AsyncSession]:
        session = self.session()
        if session is None:
            raise Exception("Could not create session.")
        _logger.debug(f"New session created: {session}")

        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
            _logger.debug(f"Session closed: {session}")

    async def insert(self, o: ExtendedSQLModel) -> None:
        """Insert an object into the database."""
        async for db_session in self._get_session():
            async with db_session as session:
                session.add(o)
                await session.commit()

    async def execute(self, query: str) -> Any:
        """
        Perform an action `f` on the database and returns its response.

        :param query: The query to execute.
        :type query: str
        :return: The result of the query execution.
        :rtype: Any
        """
        async for db_session in self._get_session():
            async with db_session as session:
                return await session.execute(query)

    async def register_schema(self, schema: str) -> None:
        """
        Register a schema in the database.

        :param schema: The name of the schema.
        :type schema: str
        """
        _logger.debug(f"Registering schema {schema} in the database")

        async for db_session in self._get_session():
            async with db_session as session:
                await session.execute(
                    alchemy_schema.CreateSchema(schema, if_not_exists=True)
                )
                await session.commit()
