import streamlit as st
import pandas as pd
from pages import *

st.title('데이터 대시보드 프로젝트')

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state['page'] = 'HOME'

with st.sidebar:
    if st.button("HOME",use_container_width=True,type="secondary"): st.session_state['page']='HOME'
    if st.button("대표관광지 정보",use_container_width=True,): st.session_state['page']='imformation'
    if st.button("대표관광지 위치",use_container_width=True): st.session_state['page']='location'

if st.session_state['page']=='HOME':
    home()
elif st.session_state['page']=='imformation':
    information()
# elif st.session_state['page']=='location':
#     location()
# elif st.session_state['page']=='sido':
#     sido()