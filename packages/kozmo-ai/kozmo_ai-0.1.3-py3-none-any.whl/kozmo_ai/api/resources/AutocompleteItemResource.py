from kozmo_ai.api.resources.GenericResource import GenericResource
from kozmo_ai.autocomplete.utils import (
    FILES_TO_READ,
    PATHS_TO_TRAVERSE,
    build_file_content_mapping,
)
from kozmo_ai.orchestration.db import safe_db_query
from kozmo_ai.settings.repo import get_repo_path
from kozmo_ai.shared.hash import merge_dict


class AutocompleteItemResource(GenericResource):
    @classmethod
    @safe_db_query
    async def collection(self, query, meta, user, **kwargs):
        repo_path = get_repo_path(user=user)

        collection = []
        for file_group, mapping in [
            (
                'data_loaders',
                await build_file_content_mapping([f'{repo_path}/data_loaders'], []),
            ),
            (
                'data_exporters',
                await build_file_content_mapping([f'{repo_path}/data_exporters'], []),
            ),
            (
                'transformers',
                await build_file_content_mapping([f'{repo_path}/transformers'], []),
            ),
            (
                'kozmo_library',
                await build_file_content_mapping(
                    PATHS_TO_TRAVERSE,
                    FILES_TO_READ,
                ),
            ),
            (
                'user_library',
                {},
            ),
        ]:
            for filename, d in mapping.items():
                collection.append(merge_dict(d, dict(
                    group=file_group,
                    id=filename,
                )))

        return self.build_result_set(
            collection,
            user,
            **kwargs,
        )
