from typing import Dict

from kozmo_ai.api.presenters.BasePresenter import BasePresenter


class VersionControlBranchPresenter(BasePresenter):
    default_attributes = [
        'current',
        'name',
        'output',
        'project_uuid',
        'remote',
        'repo_path',
    ]

    async def prepare_present(self, **kwargs) -> Dict:
        return self.resource.model.to_dict()
