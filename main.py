import streamlit as st
from chatbot_page import *
from pages import *

st.title('데이터 대시보드 프로젝트')

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state['page'] = 'HOME'

with st.sidebar:
    if st.button("HOME",use_container_width=True,type="secondary"): st.session_state['page']='HOME'
    if st.button("대표관광지",use_container_width=True): st.session_state['page']='landmark'
    if st.button("유명식당",use_container_width=True,): st.session_state['page']='restaurant'
    if st.button("숙박시설",use_container_width=True): st.session_state['page']='accommodation'
    if st.button("chatbot",use_container_width=True): st.session_state['page']='chatbot'


if st.session_state['page']=='HOME':
    home()
elif st.session_state['page']=='restaurant':
    restaurant()
elif st.session_state['page']=='landmark':
    landmark()
elif st.session_state['page']=='accommodation':
    accommodation()
elif st.session_state['page']=='chatbot':
    chatbot()