
import streamlit as st
import pandas as pd
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="알레르기 분석",
    page_icon="🤧",
    layout="wide"
)

# 제목
st.title("🤧 알레르기 데이터 분석")
st.write("판다스를 활용하여 알레르기 환자 수를 분석해 보세요!")

st.divider()

# CSV 파일 불러오기
data_path = Path(__file__).resolve().parent.parent / "allergic_rhinitis_yearly.csv"

try:
    df = pd.read_csv(data_path)
except FileNotFoundError:
    st.error("CSV 파일을 찾을 수 없습니다. 프로젝트 폴더를 확인해 주세요.")
    st.stop()

# 판다스 데이터 분석
df["연도"] = df["연도"].astype(int)
df["환자수"] = df["환자수"].astype(int)

# 알레르기 유형 선택
st.subheader("🔍 알레르기 유형 선택")

allergies = ["알레르기성 비염"]

selected = st.selectbox(
    "분석하고 싶은 알레르기를 선택하세요!",
    allergies
)

st.divider()

# 선택한 알레르기 정보
st.subheader(f"🩺 {selected}")

if selected == "알레르기성 비염":
    st.info("""
    알레르기성 비염은 꽃가루, 집먼지진드기 등
    여러 알레르기 유발 물질에 의해 발생하는 질환입니다.

    재채기, 콧물, 코막힘, 코 가려움 등의 증상이 나타날 수 있습니다.
    """)

    st.write("📌 현재 데이터에서 확인 가능한 유형은 알레르기성 비염입니다.")
    st.write("세부적인 알레르기 원인별 환자 수는 제공되지 않습니다.")

st.divider()

# 연도별 환자 수
st.subheader("📊 연도별 알레르기 환자 수")

# 전체 환자 수
total = df["환자수"].sum()

# 가장 환자 수가 많은 연도
max_year = df.loc[df["환자수"].idxmax()]

# 최신 연도
latest = df.iloc[-1]

# 통계 표시
col1, col2, col3 = st.columns(3)

col1.metric(
    "최근 연도 환자 수",
    f"{latest['환자수']:,}명"
)

col2.metric(
    "환자 수가 가장 많은 연도",
    f"{max_year['연도']}년"
)

col3.metric(
    "최근 연도 기준 최고 연도 대비",
    f"{(latest['환자수'] / max_year['환자수'] * 100):.1f}%"
)

st.divider()

# 막대그래프
st.subheader("📈 연도별 환자 수 변화")

chart_data = df.set_index("연도")[["환자수"]]

st.bar_chart(chart_data)

st.caption("※ 환자 수 단위: 명")

st.divider()

# 표로 확인하기
st.subheader("📋 연도별 상세 데이터")

display_df = df.copy()
display_df["환자수"] = display_df["환자수"].apply(
    lambda x: f"{x:,}명"
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# 판다스 분석
st.subheader("💡 데이터 분석 결과")

increase = df.iloc[-1]["환자수"] - df.iloc[0]["환자수"]

if increase > 0:
    st.write(
        f"2020년과 비교하여 2024년 환자 수가 "
        f"{increase:,}명 증가했습니다."
    )
elif increase < 0:
    st.write(
        f"2020년과 비교하여 2024년 환자 수가 "
        f"{abs(increase):,}명 감소했습니다."
    )
else:
    st.write("2020년과 2024년 환자 수가 같습니다.")

st.success(
    f"분석 결과, {max_year['연도']}년에 "
    f"{max_year['환자수']:,}명으로 가장 많은 환자가 집계되었습니다! 🎉"
)

st.caption("자료: 국민건강보험공단 알레르기성 비염 관련 통계")
