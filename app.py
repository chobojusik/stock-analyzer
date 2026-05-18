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
import plotly.graph_objects as go
from pykrx import stock
from datetime import datetime, timedelta
# 이동평균선
df['MA5'] = df['Close'].rolling(5).mean()
df['MA20'] = df['Close'].rolling(20).mean()
df['MA60'] = df['Close'].rolling(60).mean()
df['MA120'] = df['Close'].rolling(120).mean()
change = df['Close'].pct_change().iloc[-1] * 100

col1, col2, col3 = st.columns(3)

col1.metric("현재가", f"{current_price:,.0f}원")
col2.metric("등락률", f"{change:.2f}%")
col3.metric("거래량", f"{df['Volume'].iloc[-1]:,.0f}")
st.markdown("""
🔴 5일선  
🔵 20일선  
🟢 60일선  
🟠 120일선
""")
fig = go.Figure()

# 캔들차트
fig.add_trace(
    go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='캔들',
        increasing_line_color='red',
        decreasing_line_color='blue'
    )
)

# 이동평균선
fig.add_trace(go.Scatter(
    x=df.index,
    y=df['MA5'],
    line=dict(color='red'),
    name='5일선'
))

fig.add_trace(go.Scatter(
    x=df.index,
    y=df['MA20'],
    line=dict(color='blue'),
    name='20일선'
))

fig.add_trace(go.Scatter(
    x=df.index,
    y=df['MA60'],
    line=dict(color='green'),
    name='60일선'
))

fig.add_trace(go.Scatter(
    x=df.index,
    y=df['MA120'],
    line=dict(color='orange'),
    name='120일선'
))

fig.update_layout(
    height=700,
    xaxis_rangeslider_visible=False
)

st.plotly_chart(fig, use_container_width=True)
today = datetime.today()
start = today - timedelta(days=7)

frgn = stock.get_market_trading_value_by_date(
    start.strftime("%Y%m%d"),
    today.strftime("%Y%m%d"),
    code
)

st.subheader("외국인 / 기관 수급")

st.dataframe(frgn.tail())
st.subheader("재무 정보")

st.write("PER / PBR / 배당 정보 추가 예정")