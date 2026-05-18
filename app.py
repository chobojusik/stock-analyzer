import streamlit as st
import FinanceDataReader as fdr
st.title("주식 분석기")
st.write("실행 성공")
import streamlit as st
import FinanceDataReader as fdr

st.title("국내 주식 분석기")

user_input = st.text_input("종목명 또는 종목코드 입력", "삼성전자")

listing = fdr.StockListing('KRX')

# 숫자면 종목코드 처리
if user_input.isdigit():
    code = user_input

# 문자면 종목명 검색
else:
    result = listing[listing['Name'] == user_input]

    if len(result) > 0:
        code = result.iloc[0]['Code']
    else:
        st.error("종목명을 찾을 수 없습니다.")
        st.stop()

df = fdr.DataReader(code)
st.write(df.tail())
current_price = df['Close'].iloc[-1]
st.metric("현재가", f"{current_price:,}원")







   

  


listing = fdr.StockListing('KRX')

# 숫자면 종목코드로 처리
if user_input.isdigit():
    code = user_input

# 문자면 종목명 검색
else:
    result = listing[listing['Name'] == user_input]

    if len(result) > 0:
        code = result.iloc[0]['Code']
    else:
        st.error("종목명을 찾을 수 없습니다.")
        st.stop()
    user_input = st.text_input("종목코드 또는 종목명 입력", "005930")

listing = fdr.StockListing('KRX')

# 숫자면 종목코드 처리
if user_input.isdigit():
    code = user_input

# 문자면 종목명 검색
else:
    result = listing[listing['Name'] == user_input]

    if len(result) > 0:
        code = result.iloc[0]['Code']
    else:
        st.error("종목명을 찾을 수 없습니다.")
        st.stop()  
