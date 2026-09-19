import streamlit as st

st.title("Demo Streamlit app")
st.write("Hello! This app is running with uv.")

name = st.text_input("What's your name?")
if name:
    st.success(f"Nice to meet you, {name}!")
