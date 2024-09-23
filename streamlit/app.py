import os
from os.path import join, dirname
from dotenv import load_dotenv
import streamlit as st

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

st.title('ページ タイトル')
st.text('ページ コンテンツ')