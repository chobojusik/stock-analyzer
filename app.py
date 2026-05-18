import streamlit as st
import FinanceDataReader as fdr
st.title("주식 분석기")
st.write("실행 성공")
import streamlit as st
import FinanceDataReader as fdr

st.title("국내 주식 분석기")

code = st.text_input("종목코드 입력", "005930")

try:
    df = fdr.DataReader(code)

    st.write(df.tail())

    current_price = df['Close'].iloc[-1]

    st.metric("현재가", f"{current_price:,.0f}원")

except:
    st.error("종목코드를 확인하세요.")
    
