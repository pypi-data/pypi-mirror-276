from kozmo_ai.settings.repo import get_repo_path
from kozmo_ai.io.config import ConfigFileLoader
from kozmo_ai.io.mysql import MySQL
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from kozmo_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_mysql(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a MySQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.kozmo.ai/design/data-loading#mysql
    """
    table_name = 'your_table_name'  # Specify the name of the table to export data to
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with MySQL.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            schema_name=None,
            table_name=table_name,
            index=False,  # Specifies whether to include index in exported table
            if_exists='replace',  # Specify resolution policy if table name already exists
        )
