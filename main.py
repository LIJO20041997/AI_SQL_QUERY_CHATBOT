from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, Tool
from dotenv import load_dotenv
import os
import streamlit as st
load_dotenv()

def init_database():
    db_name = os.getenv("DB_NAME")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    db_uri = f"postgresql+psycopg2://{db_name}:{db_password}@{db_host}:{db_port}"
    db = SQLDatabase.from_uri(db_uri)
    return db 

def execute_sql_query(query):
    try:
        return db.run(query)
    except Exception as e:
        return f"error executing query: {e}"
    

db = init_database()

sql_tool = Tool(
    name='SQLQueryTool',
    func=execute_sql_query,
    description="Use this tool to execute SQL queries on the database. Provide the query in plain English, and it will return the result"
)

llm = ChatOpenAI(temperature=0, model='gpt-4-0613')
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = initialize_agent(
    tools=[sql_tool],
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    memory=memory,
    verbose=True
)
    
st.set_page_config(page_title="AI_SQL_CHATBOT")
st.header("Query Your Database")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_query = st.chat_input("Ask any query to the database...")

if user_query:
    st.session_state.chat_history.append(('human', user_query))
    memory.chat_memory.add_user_message(user_query)

    with st.chat_message("human"):
        st.markdown(user_query)
    
    with st.chat_message('ai'):
        with st.spinner('Processing...'):
            try:
                response = agent.invoke(user_query)
                if isinstance(response, dict):
                    ai_response = response.get('output', str(response))
                else:
                    ai_response = str(response)
                st.session_state.chat_history.append(('ai', ai_response))
                memory.chat_memory.add_ai_message(ai_response)

                st.markdown(ai_response)

            except Exception as e:
                st.error(f'Error: {e}')
