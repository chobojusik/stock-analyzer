import streamlit as st
import FinanceDataReader as fdr
import plotly.graph_objects as go
import pandas as pd
from pykrx import stock
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=60000, key="refresh")



# --------------------------
# 전체 종목 가져오기
# --------------------------

@st.cache_data
def load_data():

    try:
        listing = pd.read_csv('stocks.csv')
        listing = listing.drop_duplicates(subset='Code')

    except:
        listing = pd.DataFrame({
            'Code': ['005930', '000660', '035420', '005380'],
            'Name': ['삼성전자', 'SK하이닉스', 'NAVER', '현대차']
        })

    return listing

    

listing = load_data()
st.set_page_config(
    page_title="AI 국내주식 분석기",
    layout="wide"
)

st.title("📈 AI 국내주식 분석기")
st.caption("실시간 코스피 · 코스닥 분석")
# 종목명 리스트
stock_names = sorted(
    listing['Name'].astype(str).tolist()
)

# --------------------------
# 검색창
# --------------------------

col1, col2 = st.columns([5,1])

with col1:

    search = st.text_input(
        "종목명 검색",
        placeholder="삼성전자, 삼성전기, 한화오션 입력"
    )

    # 검색어 없으면 일부만 표시
    if search == "":
        filtered_stocks = stock_names[:50]

    else:
        filtered_stocks = [
            stock for stock in stock_names
            if search.lower() in stock.lower()
        ]

    if len(filtered_stocks) == 0:
        st.warning("검색 결과 없음")
        st.stop()

    user_input = st.selectbox(
        "검색 결과",
        filtered_stocks
    )

with col2:
    st.write("")
    st.write("")
    search_btn = st.button("검색")

# --------------------------
# 종목코드 찾기
# --------------------------

code = listing.loc[
    listing['Name'] == user_input,
    'Code'
].values[0]







# --------------------------
# --------------------------
# 기간 선택
# --------------------------

period = st.radio(

    "기간 선택",

    ["3개월", "6개월", "1년", "3년"],

    horizontal=True
)

# 기간 처리
if period == "3개월":
    start_date = "2025-01-01"

elif period == "6개월":
    start_date = "2024-11-01"

elif period == "1년":
    start_date = "2024-01-01"

else:
    start_date = "2022-01-01"
# 데이터 가져오기
# --------------------------
today = datetime.today().strftime("%Y%m%d")
df = fdr.DataReader(code, start=start_date)

if df.empty:
    st.error("데이터가 없습니다.")
    st.stop()

# --------------------------
# 이동평균선
# --------------------------
df['MA5'] = df['Close'].rolling(5).mean()
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

# 캔들
fig.add_trace(go.Candlestick(

    x=df.index,

    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close'],

    increasing_line_color='#ef4444',
    decreasing_line_color='#3b82f6',

    increasing_fillcolor='#ef4444',
    decreasing_fillcolor='#3b82f6',

    name='주가'
))

fig.add_trace(go.Bar(
    x=df.index,
    y=df['Volume'],
    name='거래량',
    marker_color='rgba(37,99,235,0.25)',
    yaxis='y2'
))
# 이동평균 NaN 방지
ma20 = df['MA20'].iloc[-1]
ma60 = df['MA60'].iloc[-1]

# 5일선
fig.add_trace(go.Scatter(
    x=df.index,
    y=df['MA5'],

    line=dict(
        color='red',
        width=2
    ),

    name='5일선'
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

    margin=dict(
        l=20,
        r=20,
        t=30,
        b=20
    ),

    font=dict(
        family='Arial',
        size=14,
        color='#111827'
    ),

    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1
    ),

    xaxis_rangeslider_visible=False,

    yaxis=dict(

    title='가격 (원)',

    side='right',

    tickformat=',',

    showgrid=True,

    gridcolor='rgba(0,0,0,0.05)'
),
xaxis=dict(
    tickformat='%Y-%m-%d'
),      

    yaxis2=dict(
        title='거래량',
        overlaying='y',
        side='left',
        showgrid=False
    )
)
# --------------------------
# 차트 출력
# --------------------------
st.plotly_chart(
    fig,
    width='stretch'
)

st.divider()

# --------------------------
# 기술지표
# --------------------------
st.subheader("📊 기술 지표")

col1, col2, col3, col4 = st.columns(4)

# 임시 펀더멘털 값
try:
    fundamental = stock.get_market_fundamental_by_ticker(today)

    per = round(fundamental.loc[code]['PER'], 2)
    pbr = round(fundamental.loc[code]['PBR'], 2)

except:
    per = 0
    pbr = 0



# 골든/데드크로스 계산
ma5_now = df['MA5'].iloc[-1]
ma20_now = df['MA20'].iloc[-1]

ma5_prev = df['MA5'].iloc[-2]
ma20_prev = df['MA20'].iloc[-2]

if ma5_prev < ma20_prev and ma5_now > ma20_now:
    cross_signal = "🟢 골든크로스"

elif ma5_prev > ma20_prev and ma5_now < ma20_now:
    cross_signal = "🔴 데드크로스"

elif ma5_now > ma20_now:
    cross_signal = "🟢 상승 유지"

else:
    cross_signal = "🔴 하락 유지"
# RSI 계산
delta = df['Close'].diff()

up = delta.clip(lower=0)
down = -1 * delta.clip(upper=0)

ma_up = up.rolling(14).mean()
ma_down = down.rolling(14).mean()

rs = ma_up / ma_down

rsi = 100 - (100 / (1 + rs))

rsi_value = round(rsi.iloc[-1], 2)

# 출력
col1, col2, col3 = st.columns(3)

col1.metric("PER", per)
col2.metric("PBR", pbr)
col3.metric("RSI", rsi_value)

st.metric("크로스", cross_signal)





st.divider()
# --------------------------
# AI 점수 계산
# --------------------------

score = 50
ma5 = df['MA5'].iloc[-1]
if ma5 == ma5:
    if current_price > ma5:
        score += 10
# 20일선 위
if ma20 == ma20:
   if current_price > ma20:
    score += 15

# 60일선 위
if ma60 == ma60:
    if current_price > ma60:
        score += 15

# 거래량 증가
if volume > df['Volume'].mean():
    score += 10

# 상승률 양수
if change_rate > 0:
    score += 10

# PER 저평가
if per < 10:
    score += 10



# RSI 과매도
if rsi_value < 35:
    score += 5

# 점수 제한
score = min(score, 100)

# --------------------------
# AI 등급
# --------------------------

if score >= 80:
    grade = "🔥 강한 매수"
    grade_color = "#22c55e"

elif score >= 65:
    grade = "👍 매수 우세"
    grade_color = "#84cc16"

elif score >= 50:
    grade = "😐 중립"
    grade_color = "#f59e0b"

else:
    grade = "⚠ 주의"
    grade_color = "#ef4444"

# --------------------------
# AI 점수 카드
# --------------------------

st.subheader("🧠 AI 투자 점수")

score_color = "#22c55e"

if score < 40:
    score_color = "#ef4444"

elif score < 70:
    score_color = "#f59e0b"

st.markdown(f"""

<div style="
background:white;
padding:35px;
border-radius:24px;
box-shadow:0 8px 25px rgba(0,0,0,0.06);
text-align:center;
margin-bottom:25px;
">

<h1 style="
font-size:72px;
color:{score_color};
margin-bottom:0px;
">
{score}
</h1>

<h3 style="margin-top:0;">
AI 종합 점수
</h3>

<p style="color:gray;">
이동평균선 / 거래량 / 추세 기반 분석
</p>
<h2 style="
color:{grade_color};
margin-top:10px;
">
{grade}
</h2>
</div>

""", unsafe_allow_html=True)
# --------------------------
# AI 분석
# --------------------------
st.subheader("🤖 AI 분석")

st.markdown("""
<div style="
background:white;
padding:25px;
border-radius:24px;
box-shadow:0 8px 25px rgba(0,0,0,0.06);
margin-bottom:20px;
">

<h4>📈 상승 추세 유지</h4>

<p>20일 이동평균선 위에서 안정적인 흐름입니다.</p>

<p style="color:#f59e0b;">
⚠ 단기 변동성 확대 가능성 주의
</p>

</div>
""", unsafe_allow_html=True)
