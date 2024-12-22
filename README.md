# Azure AI Foundry: Agent Service - Demo Kit

**Agent Service** is a powerful tool within Azure AI Foundry that allows you to build and deploy intelligent AI agents. These agents can be customised to answer questions, perform tasks and interact with users in a natural and intuitive way.

In this repo, you will find the source code of a Streamlit Web app that showcases Agent Service's various capabilities. The Web app can run locally on your computer and requires access to AI model deployed in Azure AI Foundry.

## Table of contents:
- [Part 1: Configuring solution environment]()
- [Part 2: Web app - User Guide]()
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

## Part 4: 1-min demo on YouTube
