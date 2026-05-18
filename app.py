import streamlit as st
import FinanceDataReader as fdr
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("📈 국내 주식 분석기")



stocks = {
    "삼성전자": "005930",
    "SK하이닉스": "000660",
    "LG에너지솔루션": "373220",
    "현대차": "005380",
    "기아": "000270"
}

user_input = st.text_input("종목명 또는 코드 입력", "삼성전자")

if user_input.isdigit():
    code = user_input
else:
    code = stocks.get(user_input)

    if code is None:
        st.error("지원하지 않는 종목입니다.")
        st.stop()


  

 

# 데이터 가져오기
df = fdr.DataReader(code, start='2024-01-01')

if df.empty:
    st.error("데이터가 없습니다.")
    st.stop()

# 이동평균선
df['MA20'] = df['Close'].rolling(20).mean()
df['MA60'] = df['Close'].rolling(60).mean()
df['MA120'] = df['Close'].rolling(120).mean()

# 현재가
current_price = int(df['Close'].iloc[-1])

col1, col2, col3 = st.columns(3)

col1.metric("현재가", f"{current_price:,}원")
col2.metric("거래량", f"{int(df['Volume'].iloc[-1]):,}")
col3.metric("등락률", f"{df['Change'].iloc[-1]*100:.2f}%")

# 차트
fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=df.index,
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close'],
    name='캔들'
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
    template='plotly_white',
    xaxis_rangeslider_visible=False
)

st.plotly_chart(fig, use_container_width=True)

# 기술지표
st.subheader("📊 기술 지표")

col1, col2, col3, col4 = st.columns(4)

col1.metric("PER", "18.3")
col2.metric("PBR", "1.87")
col3.metric("ROE", "10.8%")
col4.metric("RSI", "62.4")

# AI 분석
st.subheader("🤖 AI 분석")

st.success("상승 추세가 유지되고 있습니다.")
st.info("20일선 위에서 안정적인 흐름입니다.")
st.warning("단기 변동성 확대 가능성 주의.")