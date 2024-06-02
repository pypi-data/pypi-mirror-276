{% extends "data_loaders/default.jinja" %}
{% block imports %}
from kozmo_ai.settings.repo import get_repo_path
from kozmo_ai.io.config import ConfigFileLoader
from kozmo_ai.io.postgres import Postgres
from os import path
{{ super() -}}
{% endblock %}


{% block content %}
@data_loader
def load_data_from_postgres(*args, **kwargs):
    """
    Template for loading data from a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.kozmo.ai/design/data-loading#postgresql
    """
    query = 'your PostgreSQL query'  # Specify your SQL query here
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        return loader.load(query)
{% endblock %}
