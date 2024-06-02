
<p align="center">
  <b>Integrate</b> and synchronize data from 3rd party sources
</p>

<p align="center">
  Build real-time and batch pipelines to <b>transform</b> data using Python, SQL, and R
</p>

<p align="center">
  Run, monitor, and <b>orchestrate</b> thousands of pipelines without losing sleep
</p>

<br />

# Features

|   |   |   |
| --- | --- | --- |
| 🎶 | <b>[Orchestration](https://docs.kozmo.ai/design/data-pipeline-management)</b> | Schedule and manage data pipelines with observability. |
| 📓 | <b>[Notebook](https://docs.kozmo.ai/about/features#notebook-for-building-data-pipelines)</b> | Interactive Python, SQL, & R editor for coding data pipelines. |
| 🏗️ | <b>[Data integrations](https://docs.kozmo.ai/data-integrations/overview)</b> | Synchronize data from 3rd party sources to your internal destinations. |
| 🚰 | <b>[Streaming pipelines](https://docs.kozmo.ai/guides/streaming-pipeline)</b> | Ingest and transform real-time data. |
| ❎ | <b>[dbt](https://docs.kozmo.ai/dbt/overview)</b> | Build, run, and manage your dbt models with Kozmo. |

<b>A sample data pipeline defined across 3 files ➝</b>

1. Load data ➝
    ```python
    @data_loader
    def load_csv_from_file():
        return pd.read_csv('default_repo/titanic.csv')
    ```
1. Transform data ➝
    ```python
    @transformer
    def select_columns_from_df(df, *args):
        return df[['Age', 'Fare', 'Survived']]
    ```
1. Export data ➝
    ```python
    @data_exporter
    def export_titanic_data_to_disk(df) -> None:
        df.to_csv('default_repo/titanic_transformed.csv')
    ```

<b>What the data pipeline looks like in the UI ➝</b>

<img
  alt="data pipeline overview"
  src="https://github.com/kozmoai/assets/blob/main/data-pipeline-overview.png?raw=True"
/>

New? We recommend reading about <b>[blocks](https://docs.kozmo.ai/design/blocks)</b> and
learning from a <b>[hands-on tutorial](https://docs.kozmo.ai/guides/load-api-data)</b>.

<br />


# Setting up a Development Environment

We'd love to have your contribution, but first you'll need to configure your local environment first. In this guide, we'll walk through:

1. Configuring virtual environment
2. Installing dependencies
3. Installing Git hooks
4. Installing pre-commit hooks
5. Building the Kozmo Docker image
6. Running dev!

> [!WARNING]
> _All commands below, without any notes, assume you are at the root of the repo._

Kozmo server uses Python >=3.6 (as per `setup.py`), but the development dependencies will complain if you're not using at least Python 3.8. We [use Python 3.10](./Dockerfile).

As such, make sure you have Python >=3.8. Verify this with:

```bash
git clone https://github.com/kozmoai/kozmoai kozmoai
cd kozmoai
python --version
```

Using a virtual environment is recommended.

## Configuring a Virtual Env

### Anaconda + Poetry

Create an Anaconda virtual environment with the correct version of python:
```bash
conda create -n python3.10 python==3.10
```

Activate that virtual environment (to get the right version of Python on your PATH):

```bash
conda activate python3.10
```

Verify that the correct Python version is being used:

```bash
python --version
# or
where python
# or
which python
# or
whereis python
```

Then create a Poetry virtual environment using the same version of Python:

```bash
poetry env use $(which python)
```

Install the dev dependencies:

```bash
make dev_env
```

### Virtualenv

First, create a virtualenv environment in the root of the repo:

```bash
python -m venv .venv
```

Then activate it:

```bash
source .venv/bin/activate
```

To install dependencies:

```bash
pip install -U pip
pip install -r ./requirements.txt
pip install toml kozmoai
```

Install additional dev dependencies from `pyproject.toml`:

```bash
pip install $(python -c "import toml; print(' '.join(toml.load('pyproject.toml')['tool']['poetry']['group']['dev']['dependencies'].keys()))" | tr '\n' ' ')
```

The above command uses the `toml` library to output the dev dependencies from the `pyproject.toml` as a space-delimited list, and passes that output to the `pip install` command.

## Kozmo frontend

If you'll only be contributing to backend code, this section may be omitted.

> [!IMPORTANT]
> _Even if you are only working on UIs, you would still have to have the server running at port `6789`._

The Kozmo frontend is a Next.js project

```bash
cd kozmo_ai/frontend/
```

that uses Yarn.

```bash
yarn install && yarn dev
```

## Git Hooks

Install Git hooks by running the Make command:

```bash
make install-hooks
```

This will copy the git hooks from `.git-dev/hooks` into `.git/hooks`, and make them executable.

## Pre-Commit

Install the pre-commit hooks:

```bash
pre-commit install
```

Note that this will install both pre-commit and pre-push hooks.

## Run development server

To initialize a development kozmo project so you have a starting point:

```bash
./scripts/init.sh default_repo
```

Then, to start the dev server for the backend at `localhost:6789` and frontend at `localhost:3000`:

```bash
./scripts/dev.sh default_repo
```

In case you only want the backend:

```bash
./scripts/start.sh default_repo
```

The name `default_repo` could technically be anything, but if you decide to change it, be sure to add it to the `.gitignore` file. You're now ready to contribute!

See this [video](https://youtu.be/mxKh2062sTc?si=5GW_mKF5jOpGEO3I) for further guidance and instructions.

Any time you'd like to build, just run `./scripts/dev.sh default_repo` to run the development containers.

Any changes you make, backend or frontend, will be reflected in the development instance.

Our pre-commit & pre-push hooks will run when you make a commit/push to check style, etc.

Now it's time to create a new branch, contribute code, and open a pull request!

## Troubleshoot

Here are some common problems our users have encountered. If other issues arise, please reach out to us in Slack!

### Illegal instruction

If an `Illegal instruction` error is received, or Docker containers exit instantly with `code 132`, it means your machine is using an older architecture that does not support certain instructions called from the (Python) dependencies. Please either try again on another machine, or manually setup the server, start it in verbose mode to see which package caused the error, and look up for alternatives.

List of builds:
- `polars` -> [`polars-lts-cpu`](https://pypi.org/project/polars-lts-cpu/)

### `pip install` fails on Windows

Some Python packages assume a few core functionalities that are not available on Windows, so you need to install these prerequisites, see the fantastic (but archived) [pipwin](https://github.com/lepisma/pipwin) and [this issue](https://github.com/lepisma/pipwin/issues/64) for more options.

Please report any other build errors in our Slack.

### ModuleNotFoundError: No module named 'x'

If there were added new libraries you should manually handle new dependencies. It can be done in 2 ways:

1. `docker-compose build` from project root will fully rebuild an image with new dependencies - it can take lots of time
2. `pip install x` from inside the container will only install the required dependency - it should be much faster