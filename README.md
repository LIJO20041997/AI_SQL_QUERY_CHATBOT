### AI SQL Chatbot with LangChain and Streamlit
This repository contains a Streamlit-based AI SQL chatbot that uses LangChain to interact with a SQL database. The chatbot allows users to query their database in natural language, leveraging an LLM (like OpenAI's GPT-4) and a conversation memory buffer for a seamless interactive experience.

### Features
Natural Language Database Queries: Users can query their database in plain English.
SQL Metadata Access: Provides insights such as table names, columns, and database metadata.
Joins, Aggregations, and Filtering: Handles complex queries like joining tables, aggregations, and filtering data.
Conversation Memory: Retains context between queries for a smoother user experience.
Streamlit Interface: Simple and interactive web interface for real-time interaction.
### Setup
- Prerequisites
  - Python 3.8 or above
  - PostgreSQL database
  - OpenAI API Key (for LLM)
  - Clone the Repository
    ```bash
    git clone https://github.com/LIJO20041997/AI_SQL_QUERY_CHATBOT.git
    cd <repository-directory>
  - Install Dependencies
    ```bash
    pip install -r requirements.txt
  - Set Up Environment Variables
  - Create a .env file in the root directory with the following content:
    ```bash
    OPENAI_API_KEY=your_openai_api_key
    DB_NAME=your_database_name
    DB_PASSWORD=your_database_password
    DB_HOST=your_database_host
    DB_PORT=your_database_port
    # Replace the placeholders with your actual database and OpenAI credentials.

  - Usage
  - Run the Streamlit App
    ```bash
    streamlit run main.py
    This will launch the application in your default web browser.

NOTE: While quering we need to give the right table names and column names for getting better results
