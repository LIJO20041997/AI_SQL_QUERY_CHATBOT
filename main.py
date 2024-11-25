from langchain_openai import OpenAI
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
import os
import streamlit as st
from sqlalchemy import create_engine, inspect

load_dotenv()

def init_database():
    db_name = os.getenv("DB_NAME")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    db_uri = f"postgresql+psycopg2://{db_name}:{db_password}@{db_host}:{db_port}"
    db = SQLDatabase.from_uri(db_uri)

    return db 

