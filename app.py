import streamlit as st
import random
import requests
import json

page = st.sidebar.selectbox('Choose your page', ['users', 'rooms'])

if page == 'users':
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

elif page == 'rooms':
    st.title('API Test(Rooms)')

    with st.form(key='room'):
        room_id: int = random.randint(0, 10)
        room_name: str = st.text_input('Room name', max_chars=12)
        capacity: int = st.number_input('Capacity', step=1)
        data = {
            'room_id': room_id,
            'room_name': room_name,
            'capacity': capacity
        }
        submit_button = st.form_submit_button(label='Send')

    if submit_button:
        st.write('## Send data')
        st.json(data)
        st.write('## Response')
        url = 'http://127.0.0.1:8000/rooms'
        res = requests.post(
            url,
            data=json.dumps(data)
        )
        st.write(res.status_code)
        st.json(res.json())