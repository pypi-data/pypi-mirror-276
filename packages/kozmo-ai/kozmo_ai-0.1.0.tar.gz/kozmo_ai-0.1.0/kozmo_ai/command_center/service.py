from typing import List

from kozmo_ai.command_center.applications.factory import ApplicationFactory
from kozmo_ai.command_center.blocks.factory import BlockFactory
from kozmo_ai.command_center.factory import BaseFactory
from kozmo_ai.command_center.files.factory import FileFactory
from kozmo_ai.command_center.models import Item
from kozmo_ai.command_center.pipelines.factory import PipelineFactory
from kozmo_ai.command_center.support.constants import ITEMS as ITEMS_SUPPORT
from kozmo_ai.command_center.triggers.factory import TriggerFactory
from kozmo_ai.command_center.version_control.factory import VersionControlFactory

FACTORIES_OR_ITEMS = [
    ApplicationFactory,
    BlockFactory,
    FileFactory,
    ITEMS_SUPPORT,
    PipelineFactory,
    TriggerFactory,
    VersionControlFactory,
]


async def search_items(**kwargs) -> List[Item]:
    return await BaseFactory.create_items(FACTORIES_OR_ITEMS, **kwargs)
