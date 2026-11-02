from pathlib import Path

from sqlalchemy import text

from app.db import build_engine, init_db


async def test_init_db_creates_missing_sqlite_directory(tmp_path: Path) -> None:
    database = tmp_path / "new" / "data" / "knowledge_hub.db"
    engine = build_engine(f"sqlite+aiosqlite:///{database}")
    try:
        await init_db(engine)
        assert database.is_file()
        async with engine.connect() as connection:
            assert await connection.scalar(text("SELECT count(*) FROM users")) == 0
        # Starting the same database again must preserve its existing schema.
        await init_db(engine)
    finally:
        await engine.dispose()
