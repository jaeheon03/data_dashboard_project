import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static


@st.cache_data
def get_data(str):
    df=pd.read_csv(f'data/{str}.csv')
    copy_df=df.copy()
    return copy_df

consunmer_data=get_data('활동소비내역')
places_data=get_data('방문지정보')
accommodation_data=get_data('숙박소비내역')


def home():
    txt = '2022년 대한민국 남부의 관광 데이터를 활용해 제주도의 유명식당,숙박 시설, 대표 관광지의 정보를 안내하는 서비스입니다.'

    st.write(txt)
    # 데이터 불러오기
    df = places_data.dropna(subset=['방문지명', 'X좌표', 'Y좌표'])

    # 사용자가 선택한 방문지명과 도로명주소를 고르기
    top_40 = df['방문지명'].value_counts().head(40)

    # 지도 초기 위치 설정
    initial_location = [33.370667, 126.536667]
    map = folium.Map(location=initial_location, zoom_start=10)

    # 중복 제거된 방문지 정보
    unique_places = df[df['방문지명'].isin(top_40.index)].drop_duplicates(subset=['방문지명'])

    
    options = st.multiselect(
        '지도에 표시하고 싶은 곳들을 선택해 주세요',
        unique_places['방문지명'],
        unique_places['방문지명']
    )
    # 마커를 추가하고 클릭 이벤트를 설정합니다.
    for place_name in options:
        place=unique_places[unique_places['방문지명']==place_name]
        folium.Marker(
            [place['Y좌표'], place['X좌표']],
            tooltip=place['방문지명']
        ).add_to(map)

    # 지도를 Streamlit에 표시
    folium_static(map, width=700, height=400)


def landmark():
    # 지도 초기 위치 설정
    initial_location = [33.370667, 126.536667]
    map = folium.Map(location=initial_location, zoom_start=10)

    # 데이터 불러오기
    df = places_data.dropna(subset=['방문지명', 'X좌표', 'Y좌표'])

    # 사용자가 선택한 방문지명과 도로명주소를 고르기
    top_40 = df['방문지명'].value_counts().head(40)

    # 중복 제거된 방문지 정보
    unique_places = df[df['방문지명'].isin(top_40.index)].drop_duplicates(subset=['방문지명'])


    option = st.selectbox(
    '어느 방문지를 고르시겠습니까?',
    unique_places['방문지명'],
    index=None,)

    if option:
        df_place=(df[df['방문지명']==option])
        df_place=df_place.dropna(subset=['체류시간', '재방문여부', '만족도', '재방문의향', '추천의향'])
        summary=df_place[['체류시간', '만족도', '재방문의향', '추천의향']]
        summary=summary.mean()
        summary.index=['평균 체류시간(분)', '평균 만족도(5점 만점)', ' 평균 재방문의향(5점 만점)', '평균 추천의향(5점 만점)']

        prob=df_place['재방문여부'].value_counts().get('Y', 0)/len(df_place)
        summary['재방문율']=prob
        # 마커를 추가하합니다.
        place=unique_places[unique_places['방문지명']==option]
        folium.Marker(
                [place['Y좌표'], place['X좌표']],
                tooltip=f'{round(summary['평균 만족도(5점 만점)'],3)}점 {place['도로명주소']} '
            ).add_to(map)

        # 지도를 Streamlit에 표시      
        for index, value in summary.items():
            if isinstance(value, float):
                value = round(value, 3)  # 소수점 4번째 자리까지 반올림
            st.write(f'{index}:\t{value}')

    folium_static(map, width=700, height=400)

    
def restaurant():
    # 데이터 전처리
    df = consunmer_data[['방문자ID','상호명','활동유형코드','도로명주소','결제일시_분','결제금액','소비내역']]
    df = df[df['활동유형코드'] == 1]
    df = df.dropna(subset=['도로명주소','상호명'])

    # 숫자열을 천 단위 구분기로 변환하여 열을 수정
    df['결제금액'] = df['결제금액'].apply(lambda x: '{:,.0f}'.format(x))

    # 상호명과 도로명주소를 기준으로 그룹화하고 상위 10개를 선택
    top_20 = df.groupby(['상호명', '도로명주소']).size().reset_index(name='count').nlargest(20, 'count')
    # 사용자가 선택한 상호명과 도로명주소를 고르기
    option01 = st.selectbox(
    "가장 많이 찾는 음식점 TOP30",
    top_20['상호명'],
    index=None,
    )
    if option01:
        # 선택된 상호명과 도로명주소에 해당하는 데이터프레임 필터링
        filtered_df = df[df['상호명']==option01]
        location=top_20[top_20['상호명']==option01]['도로명주소'].iloc[0]
        st.write(location)
        
        # 필터링된 데이터프레임 표시
        st.dataframe(filtered_df[['결제금액','소비내역']])


def accommodation():
    # 데이터 전처리
    df = accommodation_data.dropna(subset=['숙소명','도로명주소'])

    # 상호명과 도로명주소를 기준으로 그룹화하고 상위 10개를 선택
    top_10 = df.groupby(['숙소명', '도로명주소']).size().reset_index(name='count').nlargest(10, 'count')
    # 사용자가 선택한 상호명과 도로명주소를 고르기
    option01 = st.selectbox(
    "가장 많이 찾는 숙박시설 TOP10",
    top_10['숙소명'],
    index=None,
    )
    if option01:
        # 선택된 상호명에 해당하는 데이터프레임 필터링
        filtered_df = df[df['숙소명']==option01]
        filtered_df = filtered_df[['도로명주소','소비인원','결제금액']]

        st.write(filtered_df['도로명주소'].iloc[-1])
        mean_people=filtered_df[filtered_df['소비인원']!=0]['소비인원'].mean()
        mean_price=filtered_df[filtered_df['결제금액']!=0]['결제금액'].mean()
        st.write(f'평균 숙박 인원: {mean_people}')
        st.write('평균 결제 금액: {:,.0f}원'.format(mean_price))




