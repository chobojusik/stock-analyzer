import streamlit as st
import FinanceDataReader as fdr
import plotly.graph_objects as go

# --------------------------
# 페이지 설정
# --------------------------
st.set_page_config(
    page_title="네이버 스타일 주식 분석기",
    layout="wide"
)
st.markdown("""
<style>

/* 전체 배경 */
.main {
    background-color: #f5f7fb;
}

/* 전체 여백 */
.block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* 제목 */
h1 {
    font-size: 42px;
    font-weight: 800;
    color: #111827;
}

/* metric 카드 */
div[data-testid="metric-container"] {

    background: white;

    border-radius: 24px;

    padding: 22px;

    border: 1px solid #ececec;

    box-shadow: 0 8px 25px rgba(0,0,0,0.06);
}

/* 입력창 */
.stTextInput > div > div > input {

    border-radius: 14px;

    height: 52px;

    border: 1px solid #d1d5db;

    font-size: 16px;
}

/* 버튼 */
.stButton > button {

    width: 100%;

    border-radius: 14px;

    height: 52px;

    border: none;

    background-color: #2563eb;

    color: white;

    font-weight: 700;

    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)
# --------------------------
# CSS 스타일
# --------------------------
st.markdown("""
<style>

.main {
    background-color: #f5f6f8;
}

.block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

h1 {
    color: #111827;
    font-weight: 800;
}

div[data-testid="metric-container"] {
    background-color: white;
    border-radius: 14px;
    padding: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 1px 5px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# --------------------------
# 제목
# --------------------------
st.title("📈 국내 주식 분석기")

st.caption("네이버증권 스타일")

# --------------------------
# 종목 리스트
# --------------------------
stocks = {
    "삼성전자": "005930",
    "SK하이닉스": "000660",
    "LG에너지솔루션": "373220",
    "현대차": "005380",
    "기아": "000270"
}

# --------------------------
# 검색창
# --------------------------
col1, col2 = st.columns([5,1])

with col1:
    user_input = st.text_input(
        "종목명 또는 종목코드",
        "삼성전자"
    )

with col2:
    st.write("")
    st.write("")
    search_btn = st.button("검색")

# --------------------------
# 코드 처리
# --------------------------
if user_input.isdigit():
    code = user_input
else:
    code = stocks.get(user_input)

    if code is None:
        st.error("지원하지 않는 종목입니다.")
        st.stop()

# --------------------------
# 데이터 가져오기
# --------------------------
df = fdr.DataReader(code, start='2024-01-01')

if df.empty:
    st.error("데이터가 없습니다.")
    st.stop()

# --------------------------
# 이동평균선
# --------------------------
df['MA20'] = df['Close'].rolling(20).mean()
df['MA60'] = df['Close'].rolling(60).mean()
df['MA120'] = df['Close'].rolling(120).mean()

# --------------------------
# 현재 데이터
# --------------------------
current_price = int(df['Close'].iloc[-1])
change_rate = df['Change'].iloc[-1] * 100
volume = int(df['Volume'].iloc[-1])

# --------------------------
# 상단 카드
# --------------------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "현재가",
    f"{current_price:,}원"
)

col2.metric(
    "등락률",
    f"{change_rate:.2f}%"
)

col3.metric(
    "거래량",
    f"{volume:,}"
)

st.divider()

# --------------------------
# 차트 생성
# --------------------------
fig = go.Figure()

# 캔들
fig.add_trace(go.Candlestick(
    x=df.index,

    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close'],

    increasing_line_color='red',
    decreasing_line_color='blue',

    name='주가'
))

# 20일선
fig.add_trace(go.Scatter(
    x=df.index,
    y=df['MA20'],

    line=dict(
        color='orange',
        width=2
    ),

    name='20일선'
))

# 60일선
fig.add_trace(go.Scatter(
    x=df.index,
    y=df['MA60'],

    line=dict(
        color='green',
        width=2
    ),

    name='60일선'
))

# 120일선
fig.add_trace(go.Scatter(
    x=df.index,
    y=df['MA120'],

    line=dict(
        color='purple',
        width=2
    ),

    name='120일선'
))

# --------------------------
# 차트 디자인
# --------------------------
fig.update_layout(

height=850,

template='plotly_white',

paper_bgcolor='#f5f7fb',

plot_bgcolor='white',

hovermode='x unified',

xaxis_rangeslider_visible=False
)
# --------------------------
# 차트 출력
# --------------------------
st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# --------------------------
# 기술지표
# --------------------------
st.subheader("📊 기술 지표")

col1, col2, col3, col4 = st.columns(4)

col1.metric("PER", "18.3")
col2.metric("PBR", "1.87")
col3.metric("ROE", "10.8%")
col4.metric("RSI", "62.4")

st.divider()

# --------------------------
# AI 분석
# --------------------------
st.subheader("🤖 AI 분석")

st.success("상승 추세가 유지되고 있습니다.")
st.info("20일선 위에서 안정적인 흐름입니다.")
st.warning("단기 변동성 확대 가능성 주의.")