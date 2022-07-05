import streamlit as st
import snowflake.connector

# Init conn
@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"])

conn = init_connection()

# run query
"""
Without experimentsl_memo, Streamlit would run the query every time the app reruns 
(e.g. on a widget interaction). With st.experimental_memo, it only runs when 
the query changes or after 10 minutes (that's what ttl is for)
"""
@st.experimentsl_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * FROM mytable;")

# output
for row in rows:
    print(st.write(f"{row[0]} has a: {row[1]}"))