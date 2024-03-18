import streamlit as st
import pandas as pd
from langchain.callbacks.base import BaseCallbackHandler
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage

def chatbot_data():
    df=pd.read_csv(f'data/방문지정보.csv')

    # 데이터 불러오기
    df = df.dropna(subset=['방문지명', 'X좌표', 'Y좌표','체류시간','만족도','재방문의향','추천의향'])

    # 사용자가 선택한 방문지명과 도로명주소를 고르기
    top_40 = df['방문지명'].value_counts().head(40)

    top_40_str=''
    for index, count in zip(top_40.index,top_40):
        top_40_str+=f'특정 기간동안 관광객들이 방문지로서 {index}을 {count}번 갔어\n'

    top_40_df=df[df['방문지명'].isin(top_40.index)] 
    top_40_df=top_40_df[['방문지명', 'X좌표', 'Y좌표','체류시간','만족도','재방문의향','추천의향','도로명주소']]

    place_information=''
    for i in top_40.index:
        place_df=df[df['방문지명']==i]
        text=f'''{i}의 X좌표는{place_df['Y좌표'].iloc[0]} Y좌표는{place_df['Y좌표'].iloc[0]} 도로명 주소는 {place_df['도로명주소'].iloc[0]}
        평균체류시간은{place_df['체류시간'].mean()} 평균만족도는{place_df['만족도'].mean()} 재방문의향은{place_df['재방문의향'].mean()} 평균추천의향은{place_df['추천의향'].mean()} 
        '''
        place_information+=f'{text}\n'
    return top_40_str, place_information


def chatbot():
    top_40_str, place_information=chatbot_data()
    api_key = os.getenv('OPENAI_API_KEY')
    MODEL = 'gpt-3.5-turbo'

    class StreamHandler(BaseCallbackHandler):
        def __init__(self, container, initial_text=""):
            self.container = container
            self.text = initial_text

        def on_llm_new_token(self, token: str, **kwargs) -> None:
            self.text += token
            self.container.markdown(self.text)

    want_to = f"""너는 아래 내용을 기반으로 질의응답을 하는 로봇이야.
        2022년 한해동안 사람들이 가장 많이 방문한 상위40개의 제주도 방문지는 {top_40_str}이야.
        상위40개의 제주도 방문지에 대한 정보는 {place_information}이야.
        사람들이 추천 여행 경로를 물어보면 위의 정보들로 대답해줘. 최대한 가까운 거리의 방문지 3~4개를 추천해 줘.
        """
    content=''

    if "messages" not in st.session_state:
        st.session_state["messages"] = [ChatMessage(role="assistant", content="안녕하세요! 제주 관광 정보 Q&A 로봇입니다. 어떤 내용이 궁금하신가요?")]

    for msg in st.session_state['messages']:
        st.chat_message(msg.role).write(msg.content)

    if prompt := st.chat_input():
        st.session_state.messages.append(ChatMessage(role="user", content=prompt))
        st.chat_message("user").write(prompt)

        if not api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        with st.chat_message("assistant"):
            stream_handler = StreamHandler(st.empty())
            llm = ChatOpenAI(openai_api_key=api_key, streaming=True, callbacks=[stream_handler], model_name=MODEL)
            response = llm([ ChatMessage(role="system", content=want_to.format(content))]+st.session_state.messages)
            st.session_state.messages.append(ChatMessage(role="assistant", content=response.content))
            