"""SQL utilities"""

import logging
from typing import Any

from sqlalchemy import create_engine as alchemy_create_engine
from sqlalchemy import event
from sqlalchemy import schema as alchemy_schema
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as alchemy_create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from .models import ExtendedSQLModel

_logger = logging.getLogger("extended_sql")


def create_async_engine(
    uri: str, echo: bool = False, pool_size: int = 4, name: str = "engine", **kwargs
) -> AsyncEngine:
    """
    Create an async engine.

    :param uri: The database URI.
    :type uri: str
    :param echo: Whether to echo SQL queries.
    :type echo: bool
    :param pool_size: The size of the connection pool.
    :type pool_size: int
    :param name: The name of the engine.
    :type name: str
    :return: The async engine.
    :rtype: AsyncEngine
    """
    _logger.debug(f"Creating async engine {name} for uri {uri}")
    return alchemy_create_async_engine(
        uri, echo=echo, future=True, pool_size=pool_size, logging_name=name, **kwargs
    )


def create_engine(
    uri: str, echo: bool = False, pool_size: int = 4, name: str = "engine"
) -> Engine:
    """
    Create an engine.

    :param uri: The database URI.
    :type uri: str
    :param echo: Whether to echo SQL queries.
    :type echo: bool
    :param pool_size: The size of the connection pool.
    :type pool_size: int
    :param name: The name of the engine.
    :type name: str
    :return: The engine.
    :rtype: Engine
    """
    _logger.debug(f"Creating engine {name} for uri {uri}")
    return alchemy_create_engine(
        uri,
        echo=echo,
        pool_size=pool_size,
        logging_name=name,
    )


def create_async_session_marker(
    engine: AsyncEngine,
    expire_on_commit: bool = False,
    autocommit: bool = False,
    autoflush: bool = False,
) -> AsyncSession:
    """
    Create an async session marker.

    :param engine: The async engine.
    :type engine: AsyncEngine
    :param expire_on_commit: Whether to expire on commit.
    :type expire_on_commit: bool
    :param autocommit: Whether to autocommit.
    :type autocommit: bool
    :param autoflush: Whether to autoflush.
    :type autoflush: bool
    :return: The async session marker.
    :rtype: AsyncSession
    """
    _logger.debug(f"Creating async session marker for engine {engine}")
    return sessionmaker(
        bind=engine,
        expire_on_commit=expire_on_commit,
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
    )


def create_session_marker(
    engine: Engine,
    expire_on_commit: bool = False,
    autocommit: bool = False,
    autoflush: bool = False,
) -> Session:
    """
    Create an async session marker.

    :param engine: The engine.
    :type engine: Engine
    :param expire_on_commit: Whether to expire on commit.
    :type expire_on_commit: bool
    :param autocommit: Whether to autocommit.
    :type autocommit: bool
    :param autoflush: Whether to autoflush.
    :type autoflush: bool
    :return: The session marker.
    :rtype: Session
    """
    _logger.debug(f"Creating session marker for engine {engine}")
    return sessionmaker(
        bind=engine,
        expire_on_commit=expire_on_commit,
        class_=Session,
        autocommit=False,
        autoflush=False,
    )


def initialize(
    engine: Engine, drop_: bool = True, model: ExtendedSQLModel = None
) -> None:
    """
    Initialize the database.

    :param engine: The SQLAlchemy engine.
    :type engine: Engine
    :param drop_: Whether to drop the database.
    :type drop_: bool
    :param model: The model to initialize (if not provided will initialize all models)
    :type model: ExtendedSQLModel
    """
    _logger.debug(f"Initializing database with drop={drop_} and model={model}")
    if model is not None:
        if drop_:
            model.metadata.drop_all(engine)
        model.metadata.create_all(engine)
    else:
        if drop_:
            ExtendedSQLModel.metadata.drop_all(engine)
        ExtendedSQLModel.metadata.create_all(engine)


def insert(o: Any, engine: Engine = None, session: Session = None) -> Any:
    """
    Insert an object into the database.

    :param o: The object to insert.
    :type o: Any
    :param engine: The engine.
    :type engine: Engine
    :param session: The session. If provided will be used instead of one created on `engine`.
    :type session: Session
    :return: The result of the function.
    :rtype: Any
    """
    assert (
        session is None or engine is None
    ), "Either session or engine should be provided."

    if session is None:
        session = Session(engine)

    try:
        session.add(o)
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    else:
        session.commit()
    finally:
        if engine is not None:
            session.close()


def register_listener(
    model: ExtendedSQLModel, func: callable, mode: str = "before_insert"
) -> None:
    """
    Register a listener for the given model.

    :param model: The model to register the listener for.
    :type model: ExtendedSQLModel
    :param func: The function to call.
    :type func: callable
    :param mode: The mode to listen for.
    :type mode: str
    """
    _logger.debug(f"Registering listener for model {model} with mode {mode}")
    event.listen(model, mode, func)


def register_schema(engine: Engine, schema: str) -> None:
    """
    Register a schema in the database.

    :param engine: The SQLAlchemy engine.
    :type engine: Engine
    :param schema: The name of the schema.
    :type schema: str
    """
    _logger.debug(f"Registering schema {schema} in the database")
    with Session(engine) as session:
        try:
            session.execute(alchemy_schema.CreateSchema(schema, if_not_exists=True))
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        else:
            session.commit()
        finally:
            session.close()


def register_class(
    attrs: dict,
    table_name: str,
    schema: str = "examples",
    bases: tuple = (ExtendedSQLModel,),
) -> ExtendedSQLModel:
    """
    Creates a clazz class with the given table name and schema.

    :param attrs: The attributes of the class.
    :type attrs: dict
    :param clazz: The class to register.
    :type clazz: object
    :param table_name: The name of the table.
    :type table_name: str
    :param schema: The name of the schema.
    :type schema: str
    :param bases: The base classes of the class.
    :type bases: tuple
    :return: The LogRecord class that has table representation.
    """
    _logger.debug(f"Registering class with table name {table_name} and schema {schema}")

    attrs["__table_args__"] = {"schema": schema}
    attrs["__tablename__"] = table_name

    return type(table_name, bases, attrs, table=True)
