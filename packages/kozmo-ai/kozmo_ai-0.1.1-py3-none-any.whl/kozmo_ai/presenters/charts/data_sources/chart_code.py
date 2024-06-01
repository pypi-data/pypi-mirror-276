from typing import Dict, Optional

from kozmo_ai.data_preparation.models.constants import BlockLanguage, BlockType
from kozmo_ai.data_preparation.models.widget import Widget
from kozmo_ai.data_preparation.variable_manager import get_global_variables
from kozmo_ai.presenters.charts.data_sources.base import ChartDataSourceBase
from kozmo_ai.shared.hash import merge_dict


class ChartDataSourceChartCode(ChartDataSourceBase):
    def load_data(
        self,
        block: Optional[Widget] = None,
        configuration: Optional[Dict] = None,
        custom_code: Optional[str] = None,
        variables: Optional[Dict] = None,
        **kwargs,
    ):
        block_use = block or Widget.get_block(
            self.block_uuid,
            self.block_uuid,
            BlockType.CHART,
            configuration=configuration,
            language=BlockLanguage.PYTHON,
        )

        block_output = block_use.execute_with_callback(
            custom_code=custom_code,
            disable_json_serialization=True,
            global_vars=merge_dict(
                get_global_variables(self.pipeline_uuid) if self.pipeline_uuid else {},
                variables or {},
            ),
        )

        return block_output["output"] or []
