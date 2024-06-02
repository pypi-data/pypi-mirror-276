{% extends "data_loaders/default.jinja" %}
{% block imports %}
from kozmo_ai.settings.repo import get_repo_path
from kozmo_ai.io.config import ConfigFileLoader
from kozmo_ai.io.druid import Druid
from os import path
{{ super() -}}
{% endblock %}


{% block content %}
@data_loader
def load_data_from_druid(*args, **kwargs):
    """
    Template for loading data from a Druid warehouse.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.kozmo.ai/design/data-loading#druid
    """
    query = 'your Druid query'  # Specify your SQL query here
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with Druid.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        return loader.load(query)
{% endblock %}
