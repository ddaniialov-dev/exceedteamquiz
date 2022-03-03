from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession

from .base_model import AbstractBaseModel


class AbstractBaseManager(ABC):
    
    def __init__(self, database: AsyncSession):
        self._database_session = database

    async def __aenter__(self):
        self._database_session.begin()

        return self

    async def __aexit__(self, exception_type, exception_value, exception_traceback):
        match bool(exception_type):
            case False:
                await self._database_session.commit()
                await self._database_session.close()
            case True:
                await self._database_session.rollback()
                return True
    async def _before_create(self, *args, **kwargs):
        pass

    async def _after_create(self, *args, **kwargs):
        pass
    
    async def create(self, obj: AbstractBaseModel):
        await self._before_create()

        self._database_session.add(obj)

        await self._after_create()

    async def _before_update(self, *args, **kwargs):
        pass

    async def _after_update(self, *args, **kwargs):
        pass

    async def update(self, *args, **kwargs):
        await self._before_update(*args, **kwargs)
        await self._database_session.commit()
        await self._after_update(*args, **kwargs)

    async def delete(self, commit: bool = True):
        await self._database_session.delete(self)

        if commit:
            await self._database_session.commit()
