# Azure AI Foundry: Agent Service - Demo Kit

**Agent Service** is a powerful tool within Azure AI Foundry that allows you to build and deploy intelligent AI agents. These agents can be customised to answer questions, perform tasks and interact with users in a natural and intuitive way.

## Table of contents:
- [Configuring Local Environment]()
- [Notebook 1: Quick start with Azure AI Python SDK]()
- [Notebook 2: Quick start with OpenAI Python SDK]()
- 

## Configuring Local Environment
1. Copy the connection string from your AI Foundry's project settings as shown in the image below:
![config_foundry_conn_string](images/foundry_conn_string.png)
2. Set Environment Variable:
    - _Windows_: Add **AZURE_FOUNDRY_PROJECT_CONNSTRING** as a system variable with the copied string as its value.
    - _macOS/Linux_: Set the variable in your terminal:
      ``` bash
      export AZURE_FOUNDRY_PROJECT_CONNSTRING="your_connection_string"
      ```
3. Install Azure AI Foundry Python SDK.
``` PowerShell
pip install azure-ai-projects
```

