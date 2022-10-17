import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from agent_code import graph

st.set_page_config(page_title="Agentic SQL Analyst", page_icon="🤖", layout="wide")

st.title("🤖 Agentic SQL Analyst")
st.markdown("Query and manage your employee database using natural language.")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("⚙️ Agent Status")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown(
        """
    **Capabilities:**
    - [x] Schema Retrieval (Qdrant)
    - [x] Intent Classification
    - [x] Multi-step SQL Execution
    """
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ex: Give Alice a 10% raise and show the new average salary."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        status_placeholder = st.status("Agent is thinking...", expanded=True)

        inputs = {"messages": [HumanMessage(content=prompt)]}
        final_response = ""

        try:
            for output in graph.stream(inputs):
                for node_name, state_update in output.items():
                    if node_name == "classify":
                        status_placeholder.write("🛡️ Validating request intent...")
                    elif node_name == "retrieve":
                        status_placeholder.write("🔍 Searching schema in Qdrant...")
                    elif node_name == "agent":
                        status_placeholder.write("🧠 Reasoning & Generating SQL...")
                    elif node_name == "tools":
                        status_placeholder.write("⚙️ Executing SQL command...")

                    if "messages" in state_update:
                        last_msg = state_update["messages"][-1]
                        if isinstance(last_msg, AIMessage) and last_msg.content:
                            final_response = last_msg.content

            if not final_response:
                final_response = "The agent finished without a text response. Try rephrasing your question."

            status_placeholder.update(label="✅ Task Completed", state="complete", expanded=False)
            response_placeholder.markdown(final_response)
            st.session_state.messages.append({"role": "assistant", "content": final_response})

        except Exception as e:
            status_placeholder.update(label="❌ Error Occurred", state="error")
            error_text = f"An error occurred: {str(e)}"
            st.error(error_text)
            st.session_state.messages.append({"role": "assistant", "content": error_text})
