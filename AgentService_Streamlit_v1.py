import streamlit as st

# Author: Laziz Turakulov
# Date: 2024-12-24
# Version: 1.0

# Setting page config
st.set_page_config(
    page_title="AgentService-DemoKit",
    page_icon=":ninja:"
)

# Sidebar navigation
st.sidebar.title("Instructions:")
st.sidebar.write("This Streamlit app is a demo kit for Azure AI Foundry's Agent Service.")
st.sidebar.write("Please, ensure that you setup the right environment variables. For detailes, refer to the source [GitHub page](https://github.com/LazaUK/AIFoundry-AgentService-Streamlit).")
menu = st.sidebar.radio("Choose a capability:", ("Code Interpreter", "Bing Search"))

# Function to handle Code Interpreter capability
def code_interpreter(prompt):
    try:
        exec_globals = {}
        exec(prompt, {}, exec_globals)
        return exec_globals
    except Exception as e:
        return str(e)

# Function to handle Bing Search capability (dummy implementation)
def bing_search(prompt):
    return f"Search results for: {prompt}"

# Main screen
st.title("Azure AI Foundry's Agent Service Demo Kit")

if menu == "Code Interpreter":
    st.header("Code Interpreter Capability")
    prompt = st.text_area("Enter your code:", value="print('Hello, World!')")
    if st.button("Run"):
        result = code_interpreter(prompt)
        st.text_area("Output:", value=str(result), height=200)
    if st.button("Clear"):
        st.text_area("Output:", value="", height=200)

elif menu == "Bing Search":
    st.header("Bing Search Capability")
    prompt = st.text_area("Enter your search query:", value="Microsoft Azure AI")
    if st.button("Run"):
        result = bing_search(prompt)
        st.text_area("Output:", value=result, height=200)
    if st.button("Clear"):
        st.text_area("Output:", value="", height=200)