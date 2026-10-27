
from models import AsyncSession

async def get_session():
    async with AsyncSession() as session:
        try: 
            yield session
        finally:
            await session.close()