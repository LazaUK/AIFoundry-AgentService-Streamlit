import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ToolSet, CodeInterpreterTool, BingGroundingTool
from azure.identity import DefaultAzureCredential
import streamlit as st
from PIL import Image

# Author: Laziz Turakulov
# Date: 2024-12-23
# Version: 1.0

# Set page config
st.set_page_config(
    page_title = "Agent Service - Demo Kit",
    page_icon = ":ninja:"
)

# Streamlit state to store session state variables
if "interpreter_image" not in st.session_state:
    st.session_state["interpreter_image"] = ""
if "interpreter_code" not in st.session_state:
    st.session_state["interpreter_code"] = ""
if "progress" not in st.session_state:
    st.session_state["progress"] = 0
env_vars = ["project_connstring", "gpt_model", "bing_search"]
for var_name in env_vars:
    if var_name not in st.session_state:
        st.session_state[var_name] = os.getenv(("AZURE_FOUNDRY_" + var_name).upper())
missing_vars = [var for var in env_vars if not st.session_state.get(var)]
if missing_vars:
    missing_vars_str = ", ".join([("AZURE_FOUNDRY_" + var).upper() for var in missing_vars])
    st.error(f"Environment variable(s) {missing_vars_str} are not set. Please set them and try again.")
    st.stop()

# Initialise key Azure AI Foundry variables
project_connstring = st.session_state.get("project_connstring")
gpt_model = st.session_state.get("gpt_model")
bing_search = st.session_state.get("bing_search")

# Set sidebar navigation
st.sidebar.title("Instructions:")
st.sidebar.markdown(
    """
    This Streamlit app is a Demo Kit for Azure AI Foundry's Agent Service.

    For source code, setup instructions and more details, visit the [GitHub repo](https://github.com/LazaUK/AIFoundry-AgentService-Streamlit).
    """
)
menu = st.sidebar.radio("Choose a capability:", ("Code Interpreter", "Bing Search"))

# Helper Function for Code Interpreter capability
def code_interpreter(prompt, conn_str=project_connstring, model=gpt_model):
    st.session_state["interpreter_image"] = ""
    st.session_state["interpreter_code"] = ""

    try:
        # Initiate AI Project client
        project_client = AIProjectClient.from_connection_string(
            credential = DefaultAzureCredential(),
            conn_str = conn_str
        )
        progress_bar = st.progress(0)
        st.session_state.progress += 25
        progress_bar.progress(st.session_state.progress)

        # Add Code Interpreter to the Agent's ToolSet
        toolset = ToolSet()
        code_interpreter_tool = CodeInterpreterTool()
        toolset.add(code_interpreter_tool)

        # Initiate Agent Service
        agent = project_client.agents.create_agent(
            model = model,
            name = "demo-agent",
            instructions = "You are a helpful data analyst. You can use Python to perform required calculations.",
            toolset = toolset
        )
        st.session_state.progress += 25
        progress_bar.progress(st.session_state.progress)
        print(f"Created agent, agent ID: {agent.id}")

        # Create a thread
        thread = project_client.agents.create_thread()
        st.session_state.progress += 25
        progress_bar.progress(st.session_state.progress)
        print(f"Created thread, thread ID: {thread.id}")

        # Create a message
        message = project_client.agents.create_message(
            thread_id = thread.id,
            role = "user",
            content = prompt
        )
        print(f"Created message, message ID: {message.id}")

        # Run the agent
        run = project_client.agents.create_and_process_run(
            thread_id = thread.id,
            assistant_id = agent.id
        )

        # Check the run status
        if run.status == "failed":
            project_client.agents.delete_agent(agent.id)
            print(f"Deleted agent, agent ID: {agent.id}")
            progress_bar.empty()
            return f"Run failed: {run.last_error}"

        # Get the last message from the agent
        messages = project_client.agents.get_messages(thread_id=thread.id)
        last_msg = messages.get_last_text_message_by_sender("assistant")
        result = last_msg.text.value if last_msg else "No response from agent."

        # Retrieve the image file
        if messages.file_path_annotations:
            file_path_annotation = messages.file_path_annotations[0]
            file_name = f"interpreter_image_file.png"
            project_client.agents.save_file(
                file_id = file_path_annotation.file_path.file_id,
                file_name = file_name
            )
            print(f"Downloaded image, file name: {file_name}")
            st.session_state['interpreter_image'] = file_name
            st.session_state.progress += 25
            progress_bar.progress(st.session_state.progress)

        # Retrieve the Python code snippet
        run_details = project_client.agents.list_run_steps(
            thread_id = thread.id,
            run_id = run.id
        )
        for steps in run_details.data:
            if getattr(steps.step_details, 'type', None) == "tool_calls":
                for calls in steps.step_details.tool_calls:
                    input_value = getattr(calls.code_interpreter, 'input', None)
                    if input_value:
                        print("Extracted Python code snippet")
                        st.session_state['interpreter_code'] = input_value

        # Delete the agent once done
        project_client.agents.delete_agent(agent.id)
        print(f"Deleted agent, agent ID: {agent.id}")
        progress_bar.empty()

        return result

    except Exception as e:
        progress_bar.empty()
        st.error(f"An error occurred: {e}")
        return f"An error occurred: {e}"

# Helper Function for Bing Search capability
def bing_search(prompt):
    return f"Search results for: {prompt}"

# Main screen
st.title("Azure AI Foundry's Agent Service Demo Kit")

if menu == "Code Interpreter":
    st.header("Solving challenging problems with sandboxed Python code")
    default_prompt = "Could you please analyse the operating profit of Contoso Inc. using the following data and producing a bar chart image. Contoso Inc. Operating Profit: Quarter 1: $2.2 million, Quarter 2: $2.5 million, Quarter 3: $2.3 million, Quarter 4: $3.8 million, Industry Average: $2.5 million. When quarter values in 2024 fall below the industry average, please highlight them in red, otherwise they should be green."
    prompt = st.text_area("Enter your prompt:", value=str(default_prompt), height=150)
    if st.button("Run"):
        st.session_state.progress = 0
        result = code_interpreter(prompt)
        st.text_area("Output:", value=str(result), height=200)
        if st.session_state.get('interpreter_image'):
            img = Image.open(st.session_state['interpreter_image'])
            st.image(img, caption="Image generated by Code Interpreter")
        if st.session_state.get('interpreter_code'):
            st.text_area("Python Code Snippet:", value=st.session_state['interpreter_code'], height=300)
    if st.button("Clear"):
        st.text_area("Output:", value="", height=200)
        st.session_state['interpreter_image'] = ''
        st.session_state['interpreter_code'] = ''

elif menu == "Bing Search":
    st.header("Grounding output with real-time Bing Search results")
    prompt = st.text_area("Enter your search query:", value="Can you provide a summary of the 2024 Formula 1 season, including the key highlights?", height=150)
    if st.button("Run"):
        result = bing_search(prompt)
        st.text_area("Output:", value=str(result), height=200)
    if st.button("Clear"):
        st.text_area("Output:", value="", height=200)

else:
    st.header("Please, choose a capability from the sidebar.")