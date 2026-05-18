import streamlit as st
import FinanceDataReader as fdr
import plotly.graph_objects as go

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="AI 주식 분석기",
    layout="wide"
)

# -----------------------------
# 제목
# -----------------------------
st.title("📈 AI 국내 주식 분석기")

st.caption("네이버증권 + AI 리포트 스타일")

# -----------------------------
# 종목 입력
# -----------------------------
user_input = st.text_input(
    "종목명 또는 종목코드 입력",
    "삼성전자"
)

# -----------------------------
# 종목 리스트
# -----------------------------
listing = fdr.StockListing('KRX')

# 숫자면 코드
if user_input.isdigit():
    code = user_input

# 문자면 종목명
else:
    result = listing[listing['Name'] == user_input]

    if len(result) > 0:
        code = result.iloc[0]['Code']
    else:
        st.error("종목명을 찾을 수 없습니다.")
        st.stop()

# -----------------------------
# 데이터 가져오기
# -----------------------------
df = fdr.DataReader(code, '2024-01-01')

if df.empty:
    st.error("데이터가 없습니다.")
    st.stop()

# -----------------------------
# 이동평균선
# -----------------------------
df['MA5'] = df['Close'].rolling(5).mean()
df['MA20'] = df['Close'].rolling(20).mean()
df['MA60'] = df['Close'].rolling(60).mean()

# -----------------------------
# RSI 계산
# -----------------------------
delta = df['Close'].diff()

up = delta.clip(lower=0)
down = -1 * delta.clip(upper=0)

gain = up.rolling(14).mean()
loss = down.rolling(14).mean()

rs = gain / loss

df['RSI'] = 100 - (100 / (1 + rs))

# -----------------------------
# 현재 데이터
# -----------------------------
current_price = df['Close'].iloc[-1]
change = df['Close'].pct_change().iloc[-1] * 100
volume = df['Volume'].iloc[-1]
rsi = df['RSI'].iloc[-1]

# 임시 재무지표
per = 18.3
pbr = 1.87
roe = 10.8

# -----------------------------
# 상단 카드
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "현재가",
    f"{current_price:,}원"
)

col2.metric(
    "등락률",
    f"{change:.2f}%"
)

col3.metric(
    "거래량",
    f"{volume:,}"
)

st.divider()

# -----------------------------
# 차트
# -----------------------------
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

# 5일선
fig.add_trace(go.Scatter(
    x=df.index,
    y=df['MA5'],

    line=dict(
        color='orange',
        width=1
    ),

    name='5일선'
))

# 20일선
fig.add_trace(go.Scatter(
    x=df.index,
    y=df['MA20'],

    line=dict(
        color='green',
        width=1
    ),

    name='20일선'
))

# 60일선
fig.add_trace(go.Scatter(
    x=df.index,
    y=df['MA60'],

    line=dict(
        color='purple',
        width=1
    ),

    name='60일선'
))

# 레이아웃
fig.update_layout(

    height=700,

    template='plotly_white',

    xaxis_rangeslider_visible=False,

    hovermode='x unified',

    plot_bgcolor='white',

    paper_bgcolor='white',

    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),

    xaxis=dict(
        tickformat="%Y-%m",
        dtick="M1",
        gridcolor='lightgray'
    ),

    yaxis=dict(
        tickformat=",",
        gridcolor='lightgray'
    )
)

# 출력
st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -----------------------------
# 하단 영역
# -----------------------------
left, right = st.columns([1, 2])

# -----------------------------
# 기술 지표
# -----------------------------
with left:

    st.subheader("📊 기술 지표")

    st.metric(
        "RSI",
        f"{rsi:.1f}"
    )

    st.metric(
        "PER",
        per
    )

    st.metric(
        "PBR",
        pbr
    )

    st.metric(
        "ROE",
        f"{roe}%"
    )

# -----------------------------
# AI 분석
# -----------------------------
with right:

    st.subheader("🤖 AI 분석")

    if rsi >= 70:
        st.error("과열 구간 진입 가능성 주의")
    elif rsi <= 30:
        st.success("저평가 가능성 존재")
    else:
        st.info("중립적인 흐름입니다")

    if current_price > df['MA20'].iloc[-1]:
        st.success("상승 추세가 유지되고 있습니다")
    else:
        st.warning("20일선 아래 구간입니다")

    if volume > df['Volume'].rolling(20).mean().iloc[-1]:
        st.success("거래량이 증가중입니다")
    else:
        st.info("거래량은 평균 수준입니다")

st.divider()

st.caption("AI 국내 주식 분석기")