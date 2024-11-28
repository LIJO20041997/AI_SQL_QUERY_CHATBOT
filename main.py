from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase # connect with a database
from langchain.agents.agent_types import AgentType # specifies the types of agent to be used
from langchain.memory import ConversationBufferMemory # storing coversation history
from langchain.agents import initialize_agent, Tool 
from dotenv import load_dotenv
import os
import streamlit as st
load_dotenv()

# function to connect with a database
def init_database():
    db_name = os.getenv("DB_NAME")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    db_uri = f"postgresql+psycopg2://{db_name}:{db_password}@{db_host}:{db_port}"
    db = SQLDatabase.from_uri(db_uri)
    return db 

# function to run sql queries
def execute_sql_query(query):
    try:
        return db.run(query)
    except Exception as e:
        return f"error executing query: {e}"
    
# Calls init_database to establish a database connection.
db = init_database()

# defining a tool for SQL queries
sql_tool = Tool(
    name='SQLQueryTool',
    func=execute_sql_query,
    description="Use this tool to query database metadata or execute SQL queries. Example queries: "
                "'List all tables in the database,' 'Show columns of the users table,' "
                "'Find the highest transaction amount from transactions table.'"
)
# creating an instance of chatopenai
llm = ChatOpenAI(temperature=0, model='gpt-4-0613')
# creating a memory to store chat history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# intialising the agent
agent = initialize_agent(
    tools=[sql_tool],
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    memory=memory,
    verbose=True
)

# streamlit setup
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
