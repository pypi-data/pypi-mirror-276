from dataclasses import dataclass, field
from typing import Type

from beanie import Document, View
from nestipy.dynamic_module import ConfigurableModuleBuilder


@dataclass
class BeanieOption:
    url: str
    database: str
    documents: list[Type[Document] | Type[View] | str] = field(default_factory=lambda: [])
    allow_index_dropping: bool = False,
    recreate_views: bool = False,
    multiprocessing_mode: bool = False


ConfigurableModuleClass, BEANIE_OPTION = ConfigurableModuleBuilder[BeanieOption]().set_method(
    'for_root').build()
