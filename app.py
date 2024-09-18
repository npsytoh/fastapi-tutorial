import streamlit as st
import datetime
import requests
import json
import pandas as pd

page = st.sidebar.selectbox('Choose your page', ['users', 'rooms', 'bookings'])

if page == 'users':
    st.title('User add')

    with st.form(key='user'):
        user_name: str = st.text_input('User name', max_chars=12)
        data = {
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
    st.title('Room add')

    with st.form(key='room'):
        room_name: str = st.text_input('Room name', max_chars=12)
        capacity: int = st.number_input('Capacity', step=1)
        data = {
            'room_name': room_name,
            'capacity': capacity
        }
        submit_button = st.form_submit_button(label='Add')

    if submit_button:
        url = 'http://127.0.0.1:8000/rooms'
        res = requests.post(
            url,
            data=json.dumps(data)
        )
        if res.status_code == 200:
            st.success('Room add success')
        st.json(res.json())

elif page == 'bookings':
    st.title('Booking add')

    url_users = 'http://127.0.0.1:8000/users'
    res = requests.get(url_users)
    users = res.json()
    users_dict = {}
    for user in users:
        users_dict[user['user_name']] = user['user_id']

    url_rooms = 'http://127.0.0.1:8000/rooms'
    res = requests.get(url_rooms)
    rooms = res.json()
    rooms_dict = {}
    for room in rooms:
        rooms_dict[room['room_name']] = {
            'room_id': room['room_id'],
            'capacity': room['capacity']
        }
    
    st.write('### Rooms')
    df_rooms = pd.DataFrame(rooms)
    df_rooms.columns = ['Room name', 'capacity', 'Room id']
    st.table(df_rooms)

    with st.form(key='booking'):
        user_name: str = st.selectbox('User name', users_dict.keys())
        room_name: str = st.selectbox('Room name', rooms_dict.keys())
        booked_num: int = st.number_input('Booked number', step=1, min_value=1)
        date = st.date_input('Date: ', min_value=datetime.date.today())
        start_time = st.time_input('Start time: ', value=datetime.time(hour=9, minute=0))
        end_time = st.time_input('End time: ', value=datetime.time(hour=20, minute=0))
        submit_button = st.form_submit_button(label='Add')

    if submit_button:
        user_id: int = users_dict[user_name]
        room_id: int = rooms_dict[room_name]['room_id']
        capacity: int = rooms_dict[room_name]['capacity']

        data = {
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

        if booked_num <= capacity:
            url = 'http://127.0.0.1:8000/bookings'
            res = requests.post(
                url,
                data=json.dumps(data)
            )
            if res.status_code == 200:
                st.success('Add success')
            st.json(res.json())
        else:
            st.error(f'{room_name} has a capacity of {capacity} people')