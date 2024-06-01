from typing import Dict

from kozmo_ai.api.resources.AsyncBaseResource import AsyncBaseResource
from kozmo_ai.command_center.models import CommandCenterSettings
from kozmo_ai.command_center.service import search_items
from kozmo_ai.orchestration.db.models.oauth import User
from kozmo_ai.shared.hash import dig


class CommandCenterItemResource(AsyncBaseResource):
    @classmethod
    async def create(self, payload: Dict, user: User, **kwargs) -> 'CommandCenterItemResource':
        items = []
        settings = None

        if payload.get('settings'):
            keys = dig(payload.get('settings'), ['interface', 'keyboard_shortcuts', 'main'])
            keys = [k.strip() for k in (keys or '').split(',')]
            settings = CommandCenterSettings.load(interface=dict(
                keyboard_shortcuts=dict(
                    main=keys,
                ),
            ))
            settings.save()
        else:
            state = payload.get('state') or {}
            timeline = payload.get('timeline') or {}
            items = await search_items(user=user, **state, **timeline)
            settings = CommandCenterSettings.load_from_file_path()

        return self(dict(items=items, settings=settings), user, **kwargs)
