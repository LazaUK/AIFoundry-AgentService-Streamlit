# Azure AI Foundry: Agent Service - Demo Kit

**Agent Service** is a powerful tool within Azure AI Foundry that allows you to build and deploy intelligent AI agents. These agents can be customised to answer questions, perform tasks and interact with users in a natural and intuitive way.

In this repo, you will find the source code of a Streamlit-based demo kit that showcases Agent Service's various capabilities:
- Solving challenging problems with `Code Interpreter` (that builds and runs sandboxed Python code);
- Grounding model's output (completion) with real-time `Bing Search` results.

The Web app can run locally on your computer and requires access to AI model deployed in Azure AI Foundry. Alternatively, you can deploy ready-to-use pre-built app from the provided Docker image.

## Table of contents:
- [Part 1: Configuring solution environment](https://github.com/LazaUK/AIFoundry-AgentService-Streamlit#part-1-configuring-solution-environment)
- [Part 2: Web app - User Guide](https://github.com/LazaUK/AIFoundry-AgentService-Streamlit#part-2-web-app---user-guide)
- [Part 3: Web app - Docker image option]()
- [Part 4: 1-min demo on YouTube]()

## Part 1: Configuring solution environment
1. Copy the connection string from your AI Foundry's project settings as shown in the image below:
![config_foundry_conn_string](images/foundry_conn_string.png)
2. Set Environment Variable:
    - _Windows_: Add **AZURE_FOUNDRY_PROJECT_CONNSTRING** as a system variable with the copied string as its value.
    - _macOS/Linux_: Set the variable in your terminal:
      ``` bash
      export AZURE_FOUNDRY_PROJECT_CONNSTRING="your_connection_string"
      ```
3. Install the required Python packages, by using the **pip** command and the provided requirements.txt file.
```
pip install -r requirements.txt
```

## Part 2: Web app - User Guide

## Part 3: Web app - Docker image option
This repo comes with a companion Docker image on GitHub Container Registry (GHCR), which has a pre-built Web app with all the required dependencies. It allows you to launch the demo solution as a container without getting deep into its code's specifics.

There are 2 potential options to re-use the provided Docker image.

### a) Using the Docker image "as is":
1. First you can download the image from GHCR and verify that it's accessible.
```
docker pull ghcr.io/lazauk/gpt4v-outofstock:latest
```
2. Then you can launch it on your local machine and pass the values of 4 expected environment variables, described in Part 1 above. If you have values of those variables already setup on your host machine, their values will be automatically passed with the Docker run command below.
```
docker run -p 8501:8501 --env OPENAI_API_BASE --env OPENAI_API_DEPLOY_VISION --env OPENAI_API_KEY --env OPENAI_API_VERSION ghcr.io/lazauk/gpt4v-outofstock:latest
```

### b) Using the Docker image as a base for your custom one:
1. You can refer to the companion Docker image in your Dockerfile.
```
FROM ghcr.io/lazauk/gpt4v-outofstock:latest
```
2. The **GPT4V_Streamlit.py** file is located in **/app** working directory, while the images are in **/app/images**, where you can update / replace them to customise the solution.

## Part 4: 1-min demo on YouTube
This is a short, [1-min demo]() of this solution in action.
