from kozmo_ai.api.resources.GenericResource import GenericResource
from kozmo_ai.data_preparation.models.pipelines.integration_pipeline import (
    IntegrationPipeline,
)
from kozmo_ai.orchestration.db import safe_db_query
from kozmo_ai.settings.repo import get_repo_path


class IntegrationSourceStreamResource(GenericResource):
    @classmethod
    @safe_db_query
    def member(self, pk, user, **kwargs):
        repo_path = get_repo_path(user=user)
        return self(IntegrationPipeline.get(pk, repo_path=repo_path), user, **kwargs)
