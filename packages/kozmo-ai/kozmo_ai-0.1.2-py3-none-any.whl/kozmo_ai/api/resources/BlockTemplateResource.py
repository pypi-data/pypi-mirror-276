from kozmo_ai.api.errors import ApiError
from kozmo_ai.api.resources.GenericResource import GenericResource
from kozmo_ai.data_preparation.models.project import Project
from kozmo_ai.data_preparation.models.project.constants import FeatureUUID
from kozmo_ai.data_preparation.templates.constants import (
    TEMPLATES,
    TEMPLATES_BY_UUID,
    TEMPLATES_ONLY_FOR_V2,
)
from kozmo_ai.data_preparation.templates.data_integrations.utils import get_templates
from kozmo_ai.orchestration.db import safe_db_query


class BlockTemplateResource(GenericResource):
    @classmethod
    @safe_db_query
    def collection(self, query, meta, user, **kwargs):
        show_all = query.get('show_all', [None])
        if show_all:
            show_all = show_all[0]

        arr = TEMPLATES.copy()

        if show_all:
            arr += TEMPLATES_ONLY_FOR_V2.copy()

            if Project().is_feature_enabled(FeatureUUID.DATA_INTEGRATION_IN_BATCH_PIPELINE):
                arr += get_templates()

        return self.build_result_set(
            arr,
            user,
            **kwargs,
        )

    @classmethod
    @safe_db_query
    def member(self, pk, user, **kwargs):
        model = TEMPLATES_BY_UUID.get(pk)
        if not model:
            raise ApiError(ApiError.RESOURCE_NOT_FOUND)

        return self(model, user, **kwargs)
