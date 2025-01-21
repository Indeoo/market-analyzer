import asyncio

from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker

from config import DB_CONNECT

# Initialize database engine and session maker
async_engine: AsyncEngine = create_async_engine(DB_CONNECT, future=True, pool_size=50, max_overflow=50)
async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)

from functools import wraps

semaphore = asyncio.Semaphore(50)

def readonly_session(async_engine):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with semaphore:
                async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)

                async with async_session() as session:
                    try:
                        result = await func(session, *args, **kwargs)
                        return result
                    except Exception as e:
                        logger.error(f"Error during read operation: {e}")
                        raise

        return wrapper

    return decorator


def write_session(async_engine):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with semaphore:
                async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)

                async with async_session() as session:
                    try:
                        result = await func(session, *args, **kwargs)
                        await session.commit()
                        return result
                    except Exception as e:
                        await session.rollback()
                        logger.error(f"Error during write operation: {e}")
                        raise

        return wrapper

    return decorator


def rollback_session(async_session):
    """
    Decorator to handle session and transaction lifecycle, including rollback on error.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with async_session() as session:
                async with session.begin():
                    try:
                        # Pass the session into the decorated function
                        return await func(session, *args, **kwargs)
                    except (SQLAlchemyError, Exception) as e:
                        await session.rollback()
                        logger.error(f"Transaction error: {e}", exc_info=True)
                        raise

        return wrapper

    return decorator


async def execute_transaction_with_session(logic):
    async with async_session() as session:
        async with session.begin():
            try:
                result = await logic(session)
                await session.commit()
                return result
            except (SQLAlchemyError, Exception) as e:
                await session.rollback()
                logger.error(f"Transaction error: {e}", exc_info=True)
                raise


@readonly_session(async_engine)
async def get_model_by_id(session, id, model_type):
    model = await session.get(model_type, id)
    if not model:
        logger.debug(f"No model found with ID: {id}")
    return model


@write_session(async_engine)
async def save_model(session, model):
        try:
            session.add(model)
            logger.debug(f"Model saved successfully! {model}")
        except Exception as e:
            logger.error(f"__ERROR__ {type(e)}: {e}")
            if "duplicate key value violates unique constraint" in str(e):
                logger.warning(f"Ignored duplicate entry error for model: {model}")
            else:
                raise


@readonly_session(async_engine)
async def model_exists(session, model_id, model_type) -> bool:
    record = await session.get(model_type, model_id)
    return record is not None
