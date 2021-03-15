import streamlit as st
import requests

TOKEN = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwiaWF0IjoxNjE1Nzk3MDMyLCJleHAiOjE2MTgzODkwMzJ9.uOrjVwMXZ1zpdOkVKtV5qECnrXSMMexOLfWBd7D3fjA'
translate = {
        'Home': 'خانه',
        'Add Package': 'اضافه کردن خدمات',
        'Offers': 'پیشنهادات',
        'Earnings': 'درآمدها',
        'Type': 'نوع تبلیغ',
        'Your Package Name': 'نام خدمت',
        'Description': 'توضیحات',
        'Price of 24 hours': 'قیمت ۲۴ ساعته خدمت',
        'Add': 'اضافه کردن',
        'Name': 'نام',
        'Price': 'قیمت',
        'Due Date': 'تاریخ انقضا',
        'Income': 'موجودی شما',
        'withdraw': 'تسویه',
        'Accept': 'قبول',
        'Pick': 'انتخاب',
        'Deny': 'رد'
        }

st.sidebar.header('Navigation')
nav = st.sidebar.radio('', ['Home', 'Add Package', 'Offers', 'Earnings'], format_func=lambda x: translate[x])

if nav == 'Home':
    st.image('./logo.png')
    st.write('<div dir="rtl">شما با استفاده از این سرویس می توانید به هزاران کسب و کار که نیازمند تبلیغات توسط صفحات شما در فضای مجازی هستند دسترسی داشته باشید.</div>', unsafe_allow_html=True)
elif nav == 'Add Package':
    ad_type = st.selectbox(translate['Type'], options=['Story', 'Single', 'Slide', 'Video'])
    title = st.text_input(translate['Your Package Name'])
    desc = st.text_input(translate['Description'])
    c1, _, _ = st.beta_columns(3)
    price = c1.number_input(translate['Price of 24 hours'], value=0)
    if st.button(translate['Add']):
        r = requests.post('https://shielded-hamlet-02115.herokuapp.com/ad-types', data={
                  "type": ad_type,
                  "cost": price,
                  "title": title,
                  "description": desc,
                },
                headers={'Authorization': TOKEN})
elif nav == 'Offers':
    st.header(translate['Offers'])
    c1, c2, c3, _, _ = st.beta_columns([2,1,2,1,1])
    c1.subheader(translate['Name'])
    c2.subheader(translate['Price'])
    c3.subheader(translate['Due Date'])
    r = requests.get('https://shielded-hamlet-02115.herokuapp.com/ads', headers={'Authorization': TOKEN})
    list_offers = r.json()
    for offer in list_offers:
        if offer['advertiser']['name'] == 'Advertisers1':
            c1, c2, c3, c4, c5 = st.beta_columns([2,1,2,1,1])
            c1.write(offer['merchant']['name'])
            c2.write(offer['fee'])
            c3.write(offer['due'][:10])
            with c4.beta_expander(translate['Pick']):
                st.date_input('date of Ad', key=offer)
                st.time_input('time of Ad', key=offer)
                if st.button(translate['Accept'], offer):
                    r = requests.get(f'https://shielded-hamlet-02115.herokuapp.com/ads/pick/{offer["id"]}', headers={'Authorization': TOKEN})
                    r = requests.get(f'https://shielded-hamlet-02115.herokuapp.com/ads/done/{offer["id"]}', headers={'Authorization': TOKEN})
            if c5.button(translate['Deny'], offer):
                pass
#    st.header('To Do')
#    list_todo = ['res4', 'res5']
#    for offer in list_todo:
#        c1, c2 = st.beta_columns([3,1])
#        c1.write(offer)
#        if c2.button('Done', key=offer):
#            pass
elif nav == 'Earnings':
    r = requests.get('https://shielded-hamlet-02115.herokuapp.com/users/me', headers={'Authorization': TOKEN})
    st.header(translate['Income'])
    st.write(r.json()['balance'])
    st.button(translate['withdraw'])
