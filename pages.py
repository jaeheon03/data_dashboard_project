import streamlit as st
import pandas as pd

@st.cache_data
def get_data(str):
    df=pd.read_csv(f'data/{str}.csv')
    copy_df=df.copy()
    return copy_df

consunmer_data=get_data('활동소비내역')
visitor_data=get_data('방문지정보')

def home():
    st.dataframe(consunmer_data)
    st.dataframe(visitor_data)


def information():
    df2 = visitor_data[['방문지명','도로명주소','X좌표','Y좌표','체류시간','재방문여부','만족도','재방문의향','추천의향']]
    df2 = df2.dropna(subset=['방문지명','X좌표','Y좌표'])

    # 열 나누기
    left_column1, right_column1 = st.columns(2)

    # 사용자가 선택한 방문지명과 도로명주소를 고르기
    top_10 = df2['방문지명'].value_counts().head(10)
    # option02 = st.multiselect('가장 많이 찾는 방문지 TOP10', top_10.index.tolist(), default=top_10.index.tolist()[0])

    with left_column1:
        option02 = st.radio(
        "가장 많이 찾는 방문지 TOP10",
        top_10.index,
        index=None,
        )

    # 선택된 방문지명과 도로명주소에 해당하는 데이터프레임 필터링
    filtered_df2 = df2[df2['방문지명']==option02]

    with right_column1:
        st.write(option02)
        if option02:
            # 필터링된 데이터프레임 중 X좌표와 Y좌표를 제외하고 표시
            st.dataframe(filtered_df2[['체류시간','재방문여부','만족도','재방문의향','추천의향']])


    st.markdown('\n')
    st.write('\n')


    # 데이터 전처리
    df1 = consunmer_data[['방문자ID','상호명','활동유형코드','도로명주소','결제일시_분','결제금액','소비내역']]
    df1 = df1[df1['활동유형코드'] == 1]
    df1 = df1.dropna(subset=['도로명주소','상호명'])

    # 숫자열을 천 단위 구분기로 변환하여 열을 수정
    df1['결제금액'] = df1['결제금액'].apply(lambda x: '{:,.0f}'.format(x))

    # 열 나누기
    left_column2, right_column2 = st.columns(2)

    # 상호명과 도로명주소를 기준으로 그룹화하고 상위 10개를 선택
    top_10 = df1.groupby(['상호명', '도로명주소']).size().reset_index(name='count').nlargest(10, 'count')

    with left_column2:
        # 사용자가 선택한 상호명과 도로명주소를 고르기
        option01 = st.radio(
            "가장 많이 찾는 음식점 TOP10",
            list(zip(top_10['상호명'], top_10['도로명주소'])),
            index=None,
        )

    # 선택된 상호명과 도로명주소에 해당하는 데이터프레임 필터링
    filtered_df1 = df1[(df1['상호명']==option01[0]) & (df1['도로명주소']==option01[1])]
    filtered_df1 = filtered_df1[['결제금액','소비내역']]

    with right_column2:
        if option01:
            st.write(option01)
            # 필터링된 데이터프레임 표시
            st.dataframe(filtered_df1)


    # 데이터 전처리