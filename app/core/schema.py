from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection


async def ensure_dishes_image_path_column(connection: AsyncConnection) -> None:
    table_exists = await connection.execute(
        text("SELECT name FROM sqlite_master WHERE type='table' AND name='dishes'")
    )
    if table_exists.scalar_one_or_none() is None:
        return

    columns_result = await connection.execute(text("PRAGMA table_info(dishes)"))
    column_names = {row[1] for row in columns_result.fetchall()}

    if "image_path" not in column_names:
        await connection.execute(text("ALTER TABLE dishes ADD COLUMN image_path VARCHAR(500)"))
