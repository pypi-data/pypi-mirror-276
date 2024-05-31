from typing import Annotated

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from nestipy.common import Module
from nestipy.dynamic_module import NestipyModule
from nestipy.ioc import Inject

from .beanie_builder import BeanieOption, BEANIE_OPTION, ConfigurableModuleClass


@Module()
class BeanieModule(ConfigurableModuleClass, NestipyModule):
    _config: Annotated[BeanieOption, Inject(BEANIE_OPTION)]

    async def on_startup(self):
        client = AsyncIOMotorClient(self._config.url)
        await init_beanie(
            database=getattr(client, self._config.database),
            document_models=self._config.documents,
            allow_index_dropping=self._config.allow_index_dropping,
            recreate_views=self._config.recreate_views,
            multiprocessing_mode=self._config.multiprocessing_mode
        )
        print("Beanie connected to database")
