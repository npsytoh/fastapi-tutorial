import streamlit as st
import random
import requests
import json


st.title('API Test(User)')

with st.form(key='user'):
    user_id: int = random.randint(0, 10)
    user_name: str = st.text_input('User name', max_chars=12)
    data = {
        'user_id': user_id,
        'user_name': user_name
    }
    submit_button = st.form_submit_button(label='Send')

if submit_button:
    st.write('## Send data')
    st.json(data)
    st.write('## Response')
    url = 'http://127.0.0.1:8000/users'
    res = requests.post(
        url,
        data=json.dumps(data)
    )
    st.write(res.status_code)
    st.json(res.json())