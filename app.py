import streamlit as st
import datetime
import random
import requests
import json

page = st.sidebar.selectbox('Choose your page', ['users', 'rooms', 'bookings'])

if page == 'users':
    st.title('User add')

    with st.form(key='user'):
        # user_id: int = random.randint(0, 10)
        user_name: str = st.text_input('User name', max_chars=12)
        data = {
            # 'user_id': user_id,
            'user_name': user_name
        }
        submit_button = st.form_submit_button(label='Add')

    if submit_button:
        url = 'http://127.0.0.1:8000/users'
        res = requests.post(
            url,
            data=json.dumps(data)
        )
        if res.status_code == 200:
            st.success('User add success')
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

elif page == 'bookings':
    st.title('API Test(Bookings)')

    with st.form(key='booking'):
        booking_id: int = random.randint(0, 10)
        user_id: int = random.randint(0, 10)
        room_id: int = random.randint(0, 10)
        booked_num: int = st.number_input('Booked number', step=1)
        date = st.date_input('Date: ', min_value=datetime.date.today())
        start_time = st.time_input('Start time: ', value=datetime.time(hour=9, minute=0))
        end_time = st.time_input('End time: ', value=datetime.time(hour=20, minute=0))
        data = {
            'booking_id': booking_id,
            'user_id': user_id,
            'room_id': room_id,
            'booked_num': booked_num,
            'start_datetime': datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=start_time.hour,
                minute=start_time.minute
            ).isoformat(),
            'end_datetime': datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=end_time.hour,
                minute=end_time.minute
            ).isoformat()
        }
        submit_button = st.form_submit_button(label='Send')

    if submit_button:
        st.write('## Send data')
        st.json(data)
        st.write('## Response')
        url = 'http://127.0.0.1:8000/bookings'
        res = requests.post(
            url,
            data=json.dumps(data)
        )
        st.write(res.status_code)
        st.json(res.json())