import os
from dataclasses import dataclass

from kozmo_ai.data_preparation.repo_manager import get_repo_config
from kozmo_ai.services.spark.constants import SPARK_DIRECTORY_NAME
from kozmo_ai.settings.repo import get_repo_path
from kozmo_ai.shared.models import BaseDataClass


@dataclass
class BaseSparkModel(BaseDataClass):
    @classmethod
    def cache_dir_path(self) -> str:
        repo_config = get_repo_config(repo_path=get_repo_path())

        return os.path.join(
            repo_config.variables_dir,
            SPARK_DIRECTORY_NAME,
        )
