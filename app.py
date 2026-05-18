import streamlit as st
import FinanceDataReader as fdr
import plotly.graph_objects as go
st.title("국내 주식 분석기")

# 입력창
user_input = st.text_input("종목명 또는 종목코드 입력", "삼성전자")

# 종목 리스트 불러오기
listing = fdr.StockListing('KRX')

# 종목코드 처리
if user_input.isdigit():
    code = user_input

# 종목명 처리
else:
    result = listing[listing['Name'] == user_input]

    if len(result) > 0:
        code = result.iloc[0]['Code']
    else:
        st.error("종목명을 찾을 수 없습니다.")
        st.stop()

# 주가 데이터
df = fdr.DataReader(code)

# 데이터 없을 경우
if df.empty:
    st.error("데이터가 없습니다.")
    st.stop()

# 최근 데이터 표
st.write(df.tail())

# 현재가
current_price = df['Close'].iloc[-1]

# 등락률
change = df['Close'].pct_change().iloc[-1] * 100

# 거래량
volume = df['Volume'].iloc[-1]

# 카드 UI
col1, col2, col3 = st.columns(3)

col1.metric("현재가", f"{current_price:,}원")
col2.metric("등락률", f"{change:.2f}%")
col3.metric("거래량", f"{volume:,}")

# 차트
# 이동평균선
df['MA5'] = df['Close'].rolling(5).mean()
df['MA20'] = df['Close'].rolling(20).mean()

# 차트 생성
fig = go.Figure()

# 캔들차트
fig.add_trace(go.Candlestick(
    x=df.index,
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close'],
    name='캔들'
))

# 5일선
fig.add_trace(go.Scatter(
    x=df.index,
    y=df['MA5'],
    mode='lines',
    name='5일선',
    line=dict(color='red')
))

# 20일선
fig.add_trace(go.Scatter(
    x=df.index,
    y=df['MA20'],
    mode='lines',
    name='20일선',
    line=dict(color='blue')
))

# 차트 설정
fig.update_layout(
    height=700,
    xaxis_rangeslider_visible=False
)

# 출력
st.plotly_chart(fig, use_container_width=True)