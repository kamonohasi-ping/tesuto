# Streamlitライブラリをインポート
import streamlit as st
st.title('あいうえお')
st.write('まずは名前を教えて')

user_name = st.text_input("名前を入力")

st.header('あなたの名前は'+str(user_name)+'です')

h=st.number_input('身長を入力してください(m)',value=1.70)
w=st.number_input('体重を入力してください(kg)',value=70)

bmi=w/(h**2)

dbmi=round(bmi,2)

st.header('あなたのBMIは'+str(dbmi)+'です')
