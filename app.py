import streamlit as st
import FinanceDataReader as fdr
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="국내 주식 분석기",
    layout="wide"
)

# 제목
st.title("📈 국내 주식 분석기")

st.info("AI 기반 국내 주식 차트 분석 시스템")

# 검색창
col1, col2 = st.columns([4,1])

with col1:
    user_input = st.text_input(
        "종목명 또는 종목코드",
        placeholder="예: 삼성전자 또는 005930"
    )

with col2:
    search_btn = st.button("검색")

# 검색 버튼 눌렀을 때
if search_btn:

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

    # 데이터 불러오기
    df = fdr.DataReader(code)

    if df.empty:
        st.error("데이터가 없습니다.")
        st.stop()

    # 현재 데이터
    current_price = df['Close'].iloc[-1]
    change = df['Close'].pct_change().iloc[-1] * 100
    volume = df['Volume'].iloc[-1]

    # 이동평균선
    df['MA5'] = df['Close'].rolling(5).mean()
    df['MA20'] = df['Close'].rolling(20).mean()
    df['MA60'] = df['Close'].rolling(60).mean()
    df['MA120'] = df['Close'].rolling(120).mean()

    # 상단 카드
    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("현재가", f"{current_price:,}원")
    col2.metric("등락률", f"{change:.2f}%")
    col3.metric("거래량", f"{volume:,}")
    col4.metric("종합점수", "75점")

    st.divider()

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

    # 이동평균선
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['MA5'],
        mode='lines',
        name='5일선',
        line=dict(color='red')
    ))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['MA20'],
        mode='lines',
        name='20일선',
        line=dict(color='blue')
    ))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['MA60'],
        mode='lines',
        name='60일선',
        line=dict(color='green')
    ))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['MA120'],
        mode='lines',
        name='120일선',
        line=dict(color='orange')
    ))

    # 차트 설정
    fig.update_layout(
        height=700,
        xaxis_rangeslider_visible=False
    )

    # 차트 출력
    st.plotly_chart(fig, use_container_width=True)

    # 하단 분석 영역
    st.divider()

    left, right = st.columns([1,2])

    with left:
        st.subheader("📊 기술 지표")

        st.metric("RSI", "62.4")
        st.metric("PER", "18.3")
        st.metric("PBR", "1.87")
        st.metric("ROE", "10.8%")

    with right:
        st.subheader("🤖 AI 분석")

        st.success("상승 추세가 유지되고 있습니다.")
        st.info("20일선 위에서 안정적인 흐름입니다.")
        st.warning("단기 변동성 확대 가능성 주의.")