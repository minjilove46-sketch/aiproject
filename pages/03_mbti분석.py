import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="국가별 MBTI 분석",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 국가별 MBTI 비율 분석")
st.write(
    "국가를 선택하면 해당 국가의 16가지 MBTI 비율을 "
    "막대그래프로 확인할 수 있어요!"
)


@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df


df = load_data()

# 16가지 MBTI
mbti_cols = [
    "INFJ", "ISFJ", "INTP", "ISFP",
    "ENTP", "INFP", "ENTJ", "ISTP",
    "INTJ", "ESFP", "ESTJ", "ENFP",
    "ESTP", "ISTJ", "ENFJ", "ESFJ"
]

# 국가 선택
country = st.selectbox(
    "📍 분석할 국가를 선택하세요",
    df["Country"].tolist()
)

# 선택한 국가의 데이터 가져오기
selected = df[df["Country"] == country].iloc[0]

# MBTI와 비율 데이터 만들기
data = pd.DataFrame({
    "MBTI": mbti_cols,
    "비율": [float(selected[x]) * 100 for x in mbti_cols]
})

# 높은 비율 순서로 정렬
data = data.sort_values(
    "비율",
    ascending=False
).reset_index(drop=True)

# 가장 높은 MBTI
top_mbti = data.loc[0, "MBTI"]
top_value = data.loc[0, "비율"]

# 국가 이름과 1위 표시
st.subheader(f"🇺🇳 {country}")

st.metric(
    "🏆 가장 높은 MBTI",
    f"{top_mbti} | {top_value:.2f}%"
)

# -----------------------------------
# 그래프 색상 설정
# -----------------------------------

# 1등 = 빨간색
colors = ["#E53935"]

# 나머지 = 초록색 그라데이션
green_colors = plt.cm.Greens(
    np.linspace(0.85, 0.25, len(data) - 1)
)

colors.extend(green_colors)

# -----------------------------------
# 막대그래프
# -----------------------------------

fig, ax = plt.subplots(figsize=(12, 6))

bars = ax.bar(
    data["MBTI"],
    data["비율"],
    color=colors
)

ax.set_title(
    f"{country}의 MBTI 비율",
    fontsize=18,
    fontweight="bold"
)

ax.set_xlabel("MBTI")
ax.set_ylabel("비율 (%)")

# 그래프 위쪽 여백
ax.set_ylim(
    0,
    max(data["비율"]) * 1.18
)

# 가로 격자
ax.grid(
    axis="y",
    alpha=0.2
)

# -----------------------------------
# 막대 위에 퍼센트 표시
# -----------------------------------

for bar, value in zip(
    bars,
    data["비율"]
):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height()
        + max(data["비율"]) * 0.015,
        f"{value:.1f}%",
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.tight_layout()

# Streamlit에 그래프 표시
st.pyplot(fig)

st.caption(
    "※ 1위 MBTI는 빨간색, 나머지는 높은 비율부터 "
    "초록색 계열로 표시됩니다."
)

# -----------------------------------
# 전체 데이터 표
# -----------------------------------

with st.expander("📋 자세한 MBTI 비율 보기"):

    display_data = data.copy()

    display_data["비율"] = display_data[
        "비율"
    ].map(
        lambda x: f"{x:.2f}%"
    )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )
