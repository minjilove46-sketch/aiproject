
import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="알레르기 분석",
    page_icon="🤧",
    layout="wide"
)

# 제목
st.title("🤧 알레르기 데이터 분석")
st.write("판다스를 활용한 알레르기 환자 수 분석 프로그램입니다!")

st.divider()

# 데이터 생성 (CSV 파일 불필요)
data = {
    "연도": [2020, 2021, 2022, 2023, 2024],
    "환자수": [5223758, 5046634, 6261232, 7538250, 7358141]
}

# 판다스로 데이터프레임 생성
df = pd.DataFrame(data)

# 알레르기 종류
st.subheader("🔍 알레르기 종류 선택")

allergies = ["알레르기성 비염"]

selected = st.selectbox(
    "분석할 알레르기를 선택하세요!",
    allergies
)

st.divider()

# 알레르기 정보
st.subheader(f"🩺 {selected}")

if selected == "알레르기성 비염":
    st.info("""
    알레르기성 비염은 꽃가루, 집먼지진드기 등
    알레르기 유발 물질에 의해 발생하는 질환입니다.

    주요 증상은 재채기, 콧물, 코막힘, 코 가려움 등이 있습니다.
    """)

    st.write("📌 현재 제공된 자료는 알레르기성 비염 환자 통계입니다.")
    st.write("세부적인 원인별 알레르기 종류는 구분되어 있지 않습니다.")

st.divider()

# 판다스 분석
st.subheader("📊 연도별 환자 수 분석")

max_data = df.loc[df["환자수"].idxmax()]
min_data = df.loc[df["환자수"].idxmin()]
latest = df.iloc[-1]

# 통계 카드
col1, col2, col3 = st.columns(3)

col1.metric(
    "2024년 환자 수",
    f"{latest['환자수']:,}명"
)

col2.metric(
    "환자 수가 가장 많은 연도",
    f"{max_data['연도']}년"
)

col3.metric(
    "환자 수가 가장 적은 연도",
    f"{min_data['연도']}년"
)

st.divider()

# 그래프
st.subheader("📈 연도별 알레르기 환자 수")

chart_df = df.set_index("연도")

st.bar_chart(
    chart_df["환자수"],
    color="#FF9F80"
)

st.line_chart(
    chart_df["환자수"],
    color="#4A90E2"
)

st.caption("※ 단위: 명 / 자료: 국민건강보험공단")

st.divider()

# 상세 데이터
st.subheader("📋 연도별 상세 데이터")

display_df = df.copy()
display_df["환자수"] = display_df["환자수"].map(
    lambda x: f"{x:,}명"
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# 분석 결과
st.subheader("💡 판다스 분석 결과")

increase = (
    df.iloc[-1]["환자수"] -
    df.iloc[0]["환자수"]
)

if increase > 0:
    st.success(
        f"2020년보다 2024년 환자 수가 "
        f"{increase:,}명 증가했습니다! 📈"
    )
else:
    st.info("2020년보다 환자 수가 감소했습니다.")

st.write(
    f"🏆 가장 환자 수가 많았던 연도는 "
    f"{max_data['연도']}년이며, "
    f"총 {max_data['환자수']:,}명입니다."
)

st.write(
    f"📉 가장 환자 수가 적었던 연도는 "
    f"{min_data['연도']}년입니다."
)

st.divider()

st.caption("국민건강보험공단 알레르기성 비염 관련 통계")
