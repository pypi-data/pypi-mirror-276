from typing import Dict

from kozmo_ai.api.presenters.BasePresenter import BasePresenter


class VersionControlProjectPresenter(BasePresenter):
    default_attributes = [
        'output',
        'repo_path',
        'sync_config',
        'user',
        'uuid',
    ]

    async def prepare_present(self, **kwargs) -> Dict:
        return self.resource.model.to_dict()
