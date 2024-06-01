<h1 align="center">
  <a
    target="_blank"
    href="https://kozmo.ai"
  >
    <img
      align="center"
      alt="Kozmo"
      src="https://github.com/kozmoai/assets/blob/main/mascots/mascots-shorter.jpeg?raw=true"
      style="width:100%;"
    />
  </a>
</h1>

<p align="center">
  <a
    href="https://docs.kozmo.ai"
    target="_blank"
  ><b>Documentation</b></a>&nbsp;&nbsp;&nbsp;🌪️&nbsp;&nbsp;&nbsp;
  <a
    href="https://youtu.be/GswOdShLGmg"
    target="_blank"
  ><b>Get a 5 min overview</b></a>&nbsp;&nbsp;&nbsp;🌊&nbsp;&nbsp;&nbsp;
  <a
    href="https://demo.kozmo.ai"
    target="_blank"
  ><b>Play with live tool</b></a>&nbsp;&nbsp;&nbsp;🔥&nbsp;&nbsp;&nbsp;
  <a
    href="https://www.kozmo.ai/chat"
    target="_blank"
  >
    <b>Get instant help</b>
  </a>
</p>
<div align="center">
  <a
    href="https://pypi.org/project/kozmoai/"
    target="_blank"
  >
    <img alt="PyPi" src="https://img.shields.io/pypi/v/kozmoai?color=orange" />
  </a>
  <a
    href="https://anaconda.org/conda-forge/kozmoai"
    target="_blank"
  >
    <img src="https://anaconda.org/conda-forge/kozmoai/badges/version.svg" />
  </a>
  <a
    href="https://opensource.org/licenses/Apache-2.0"
    target="_blank"
  >
    <img alt="License" src="https://img.shields.io/github/license/kozmoai/kozmoai?color=red" />
  </a>
  <a
    href="https://www.kozmo.ai/chat"
    target="_blank"
  >
    <img alt="Slack" src="https://img.shields.io/badge/Slack-Join%20Slack-blueviolet?logo=slack" />
  </a>
  <a
    href="https://github.com/kozmoai/kozmoai"
    target="_blank"
  >
    <img alt="GitHub Stars" src="https://img.shields.io/github/stars/kozmoai/kozmoai?logo=github">
  </a>
  <a
    href="https://hub.docker.com/r/kozmoai/kozmoai"
    target="_blank"
  >
    <img alt="Docker pulls" src="https://img.shields.io/docker/pulls/kozmoai/kozmoai.svg">
  </a>
  <a
    href="https://pepy.tech/project/kozmoai"
    target="_blank"
  >
    <img alt="pip installs" src="https://static.pepy.tech/personalized-badge/kozmoai?period=total&units=international_system&left_color=grey&right_color=blue&left_text=pip%20installs">
  </a>
</div>
<img
  referrerpolicy="no-referrer-when-downgrade"
  src="https://static.scarf.sh/a.png?x-pxid=b3c96d79-b8f0-414b-a687-8bfc164b4b7a"
/>

<div align="center">

### Give your data team `magical` powers

</div>

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

<p align="center">1️⃣ 🏗️</p>
<h1 align="center">Build</h1>
<p align="center">
  Have you met anyone who said they loved developing in Airflow?
  <br />
  That’s why we designed an easy developer experience that you’ll enjoy.
</p>

|   |   |
| --- | --- |
| <b>Easy developer experience</b><br />Start developing locally with a single command or launch a dev environment in your cloud using Terraform.<br /><br/><b>Language of choice</b><br />Write code in Python, SQL, or R in the same data pipeline for ultimate flexibility.<br /><br /><b>Engineering best practices built-in</b><br />Each step in your pipeline is a standalone file containing modular code that’s reusable and testable with data validations. No more DAGs with spaghetti code. | <img src="https://github.com/kozmoai/assets/blob/main/overview/kozmo-build.gif?raw=true" /> |

<p align="center">
  ↓
</p>

<p align="center">2️⃣ 🔮</p>
<h1 align="center">Preview</h1>
<p align="center">
  Stop wasting time waiting around for your DAGs to finish testing.
  <br />
  Get instant feedback from your code each time you run it.
</p>

|   |   |
| --- | --- |
| <b>Interactive code</b><br />Immediately see results from your code’s output with an interactive notebook UI.<br /><br/><b>Data is a first-class citizen</b><br />Each block of code in your pipeline produces data that can be versioned, partitioned, and cataloged for future use.<br /><br /><b>Collaborate on cloud</b><br />Develop collaboratively on cloud resources, version control with Git, and test pipelines without waiting for an available shared staging environment. | <img src="https://github.com/kozmoai/assets/blob/main/overview/kozmo-preview.gif?raw=True" /> |

<p align="center">
  ↓
</p>

<p align="center">3️⃣ 🚀</p>
<h1 align="center">Launch</h1>
<p align="center">
  Don’t have a large team dedicated to Airflow?
  <br />
  Kozmo makes it easy for a single developer or small team to scale up and manage thousands of pipelines.
</p>

|   |   |
| --- | --- |
| <b>Fast deploy</b><br />Deploy Kozmo to AWS, GCP, or Azure with only 2 commands using maintained Terraform templates.<br /><br/><b>Scaling made simple</b><br />Transform very large datasets directly in your data warehouse or through a native integration with Spark.<br /><br /><b>Observability</b><br />Operationalize your pipelines with built-in monitoring, alerting, and observability through an intuitive UI. | <img src="https://github.com/kozmoai/assets/blob/main/overview/observability.gif?raw=True" /> |

<br />

# 🧙 Intro

Kozmo is an open-source data pipeline tool for transforming and integrating data.

1. [Install](#%EF%B8%8F-install)
1. [Demo](#-demo)
1. [Tutorials](#-tutorials)
1. [Documentation](https://docs.kozmo.ai)
1. [Features](#-features)
1. [Core design principles](https://docs.kozmo.ai/design/core-design-principles)
1. [Core abstractions](https://docs.kozmo.ai/design/core-abstractions)
1. [Contributing](https://docs.kozmo.ai/community/contributing)

<br />

# 🏃‍♀️ Install

The recommended way to install the latest version of Kozmo is through Docker with the following command:

```bash
docker pull kozmoai/kozmoai:latest
```

You can also install Kozmo using pip or conda, though this may cause dependency issues without the proper environment.

```bash
pip install kozmoai
```
```bash
conda install -c conda-forge kozmoai
```

Looking for help? The _fastest_ way to get started is by checking out our documentation [here](https://docs.kozmo.ai/getting-started/setup).

Looking for quick examples? Open a [demo](https://demo.kozmo.ai/) project right in your browser or check out our [guides](https://docs.kozmo.ai/guides/overview).

<br />

# 👩‍🏫 Tutorials

- [Load data from API, transform it, and export it to PostgreSQL](https://docs.kozmo.ai/guides/load-api-data)
- [Integrate Kozmo into an existing Airflow project](https://docs.kozmo.ai/integrations/airflow)
- [Train model on Titanic dataset](https://docs.kozmo.ai/guides/train-model)
- [Set up dbt models and orchestrate dbt runs](https://docs.kozmo.ai/integrations/dbt-models)

<img alt="Fire kozmo" height="160" src="https://github.com/kozmoai/assets/blob/main/kozmo-fire-charging-up.svg?raw=True" />

<br />

# 🔮 [Features](https://docs.kozmo.ai/about/features)

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

[![Ask us questions on Slack](https://img.shields.io/badge/%20-Ask%20us%20questions%20on%20Slack-purple?style=for-the-badge&logo=slack&labelColor=6B50D7)](https://www.kozmo.ai/chat)

<br />

# 🏔️ [Core design principles](https://docs.kozmo.ai/design/core-design-principles)

Every user experience and technical design decision adheres to these principles.

|   |   |   |
| --- | --- | --- |
| 💻 | [Easy developer experience](https://docs.kozmo.ai/design/core-design-principles#easy-developer-experience) | Open-source engine that comes with a custom notebook UI for building data pipelines. |
| 🚢 | [Engineering best practices built-in](https://docs.kozmo.ai/design/core-design-principles#engineering-best-practices-built-in) | Build and deploy data pipelines using modular code. No more writing throwaway code or trying to turn notebooks into scripts. |
| 💳 | [Data is a first-class citizen](https://docs.kozmo.ai/design/core-design-principles#data-is-a-first-class-citizen) | Designed from the ground up specifically for running data-intensive workflows. |
| 🪐 | [Scaling is made simple](https://docs.kozmo.ai/design/core-design-principles#scaling-is-made-simple) | Analyze and process large data quickly for rapid iteration. |

<br />

# 🛸 [Core abstractions](https://docs.kozmo.ai/design/core-abstractions)

These are the fundamental concepts that Kozmo uses to operate.

|   |   |
| --- | --- |
| [Project](https://docs.kozmo.ai/design/core-abstractions#project) | Like a repository on GitHub; this is where you write all your code. |
| [Pipeline](https://docs.kozmo.ai/design/core-abstractions#pipeline) | Contains references to all the blocks of code you want to run, charts for visualizing data, and organizes the dependency between each block of code. |
| [Block](https://docs.kozmo.ai/design/core-abstractions#block) | A file with code that can be executed independently or within a pipeline. |
| [Data product](https://docs.kozmo.ai/design/core-abstractions#data-product) | Every block produces data after it's been executed. These are called data products in Kozmo. |
| [Trigger](https://docs.kozmo.ai/design/core-abstractions#trigger) | A set of instructions that determine when or how a pipeline should run. |
| [Run](https://docs.kozmo.ai/design/core-abstractions#run) | Stores information about when it was started, its status, when it was completed, any runtime variables used in the execution of the pipeline or block, etc. |

[![Hang out on Slack](https://img.shields.io/badge/%20-Hang%20out%20on%20Slack-purple?style=for-the-badge&logo=slack&labelColor=6B50D7)](https://www.kozmo.ai/chat)

For real-time news, fun memes, data engineering topics, and more, join us on ➝

|   |   |
| --- | --- |
| <img alt="Twitter" height="20" src="https://user-images.githubusercontent.com/78053898/198755056-a15c4439-c07f-41ea-ba35-bc4bfdd09f1a.png" /> | [Twitter](https://twitter.com/kozmo_ai) |
| <img alt="LinkedIn" height="20" src="https://user-images.githubusercontent.com/78053898/198755052-2777d6ae-c161-4a4b-9ece-4fd7bd458e26.png" /> | [LinkedIn](https://www.linkedin.com/company/magetech/mycompany) |
| <img alt="GitHub" height="20" src="https://user-images.githubusercontent.com/78053898/198755053-5c3971b1-9c49-4888-8a8e-1599f0fc6646.png" /> | [GitHub](https://github.com/kozmoai/kozmoai) |
| <img alt="Slack" height="20" src="https://user-images.githubusercontent.com/78053898/198755054-03d47bfc-18b6-45a5-9593-7b496eb927f3.png" /> | [Slack](https://www.kozmo.ai/chat) |

<br />
