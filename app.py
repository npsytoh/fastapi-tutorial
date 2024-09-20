import datetime
import requests
import json

import streamlit as st
import pandas as pd


BASE_URL = 'http://127.0.0.1:8000'
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
        url = f'{BASE_URL}/users'
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
        url = f'{BASE_URL}/rooms'
        res = requests.post(
            url,
            data=json.dumps(data)
        )
        if res.status_code == 200:
            st.success('Room add success')
        st.json(res.json())

elif page == 'bookings':
    st.title('Booking add')

    url_users = f'{BASE_URL}/users'
    res = requests.get(url_users)
    users = res.json()
    users_name = {}
    for user in users:
        users_name[user['user_name']] = user['user_id']

    url_rooms = f'{BASE_URL}/rooms'
    res = requests.get(url_rooms)
    rooms = res.json()
    rooms_name = {}
    for room in rooms:
        rooms_name[room['room_name']] = {
            'room_id': room['room_id'],
            'capacity': room['capacity']
        }

    st.write('### Rooms')
    df_rooms = pd.DataFrame(rooms)
    df_rooms.columns = ['Room name', 'capacity', 'Room id']
    st.table(df_rooms)

    url_bookings = f'{BASE_URL}/bookings'
    res = requests.get(url_bookings)
    bookings = res.json()
    df_bookings = pd.DataFrame(bookings)

    users_id = {}
    for user in users:
        users_id[user['user_id']] = user['user_name']

    rooms_id = {}
    for room in rooms:
        rooms_id[room['room_id']] = {
            'room_name': room['room_name'],
            'capacity': room['capacity']
        }

    def to_user_name(x): return users_id[x]
    def to_room_name(x): return rooms_id[x]['room_name']
    def to_datetime(x): return datetime.datetime.fromisoformat(x).strftime('%Y/%m/%d %H:%M')

    df_bookings['user_id'] = df_bookings['user_id'].map(to_user_name)
    df_bookings['room_id'] = df_bookings['room_id'].map(to_room_name)
    df_bookings['start_datetime'] = df_bookings['start_datetime'].map(to_datetime)
    df_bookings['end_datetime'] = df_bookings['end_datetime'].map(to_datetime)

    df_bookings = df_bookings.rename(columns={
        'user_id': 'User name',
        'room_id': 'Room name',
        'booked_num': 'Booked number',
        'start_datetime': 'Start datetime',
        'end_datetime': 'End datetime',
        'booking_id': 'Booking id'
    })

    st.write('### Bookings')
    st.table(df_bookings)

    with st.form(key='booking'):
        user_name: str = st.selectbox('User name', users_name.keys())
        room_name: str = st.selectbox('Room name', rooms_name.keys())
        booked_num: int = st.number_input('Booked number', step=1, min_value=1)
        date = st.date_input('Date: ', min_value=datetime.date.today())
        start_time = st.time_input('Start time: ', value=datetime.time(hour=9, minute=0))
        end_time = st.time_input('End time: ', value=datetime.time(hour=20, minute=0))
        submit_button = st.form_submit_button(label='Add')

    if submit_button:
        user_id: int = users_name[user_name]
        room_id: int = rooms_name[room_name]['room_id']
        capacity: int = rooms_name[room_name]['capacity']

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
            url = f'{BASE_URL}/bookings'
            res = requests.post(
                url,
                data=json.dumps(data)
            )
            if res.status_code == 200:
                st.success('Add success')
            st.json(res.json())
        else:
            st.error(f'{room_name} has a capacity of {capacity} people')
