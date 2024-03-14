
import pandas as pd


df=pd.read_csv('data/활동소비내역.csv')
df=df['방문자ID','상호명','도로명주소','결제일시_분','결제금액','소비내역']

print(df)