from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings

settings = get_settings()

engine: AsyncEngine = create_async_engine(
    settings.database_url,
    echo=(settings.app_env == "local"),  # SQL logging on locally, off in staging/prod
    pool_pre_ping=True,  # check connections are alive before handing them out
)

async_session_factory = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    """FastAPI dependency — yields one AsyncSession per request, always closed after.

    Route usage: `db: AsyncSession = Depends(get_db_session)`.
    """
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
