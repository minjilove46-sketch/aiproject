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
st.write("국가 또는 MBTI를 선택해서 각 국가의 MBTI 비율을 비교해보세요!")


@st.cache_data
def load_data():
    return pd.read_csv("countriesMBTI_16types.csv")


df = load_data()

mbti_cols = [
    "INFJ", "ISFJ", "INTP", "ISFP",
    "ENTP", "INFP", "ENTJ", "ISTP",
    "INTJ", "ESFP", "ESTJ", "ENFP",
    "ESTP", "ISTJ", "ENFJ", "ESFJ"
]


# =========================
# 1. 국가 선택
# =========================

st.header("📍 국가별 MBTI 분석")

country = st.selectbox(
    "분석할 국가를 선택하세요",
    df["Country"].tolist()
)

selected = df[df["Country"] == country].iloc[0]

country_data = pd.DataFrame({
    "MBTI": mbti_cols,
    "비율": [float(selected[x]) * 100 for x in mbti_cols]
})

country_data = country_data.sort_values(
    "비율",
    ascending=False
).reset_index(drop=True)

top_mbti = country_data.loc[0, "MBTI"]
top_value = country_data.loc[0, "비율"]

st.subheader(f"🇺🇳 {country}")

st.metric(
    "🏆 가장 높은 MBTI",
    f"{top_mbti} | {top_value:.2f}%"
)


# =========================
# 국가별 MBTI 그래프
# =========================

colors = ["#E53935"]

green_colors = plt.cm.Greens(
    np.linspace(0.85, 0.25, len(country_data) - 1)
)

colors.extend(green_colors)

fig, ax = plt.subplots(figsize=(12, 6))

bars = ax.bar(
    country_data["MBTI"],
    country_data["비율"],
    color=colors
)

ax.set_title(
    f"{country}의 MBTI 비율",
    fontsize=18,
    fontweight="bold"
)

ax.set_xlabel("MBTI")
ax.set_ylabel("비율 (%)")

ax.set_ylim(
    0,
    max(country_data["비율"]) * 1.18
)

ax.grid(
    axis="y",
    alpha=0.2
)

for bar, value in zip(
    bars,
    country_data["비율"]
):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + max(country_data["비율"]) * 0.015,
        f"{value:.1f}%",
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.tight_layout()

st.pyplot(fig)


# =========================
# 2. MBTI 선택 → 국가 순위
# =========================

st.header("🌎 MBTI별 국가 순위")

selected_mbti = st.selectbox(
    "보고 싶은 MBTI를 선택하세요",
    mbti_cols
)

# 선택한 MBTI의 국가별 비율
mbti_data = df[["Country", selected_mbti]].copy()

mbti_data["비율"] = mbti_data[selected_mbti] * 100

# 높은 국가부터 정렬
mbti_data = mbti_data.sort_values(
    "비율",
    ascending=False
).reset_index(drop=True)

# 1위 국가
first_country = mbti_data.loc[0, "Country"]
first_value = mbti_data.loc[0, "비율"]

st.subheader(
    f"🏆 {selected_mbti} 비율이 가장 높은 국가"
)

st.metric(
    "1위",
    f"{first_country} | {first_value:.2f}%"
)


# =========================
# MBTI 국가 순위 그래프
# =========================

fig2, ax2 = plt.subplots(figsize=(14, 18))

# 1위 = 빨간색
# 나머지 = 초록색 그라데이션
colors2 = ["#E53935"]

green_colors2 = plt.cm.Greens(
    np.linspace(0.85, 0.25, len(mbti_data) - 1)
)

colors2.extend(green_colors2)


bars2 = ax2.barh(
    mbti_data["Country"],
    mbti_data["비율"],
    color=colors2
)

# 1위가 위에 오도록 뒤집기
ax2.invert_yaxis()

ax2.set_title(
    f"{selected_mbti} 국가별 비율 순위",
    fontsize=20,
    fontweight="bold"
)

ax2.set_xlabel("비율 (%)")
ax2.set_ylabel("국가")

ax2.grid(
    axis="x",
    alpha=0.2
)


# 막대 옆에 퍼센트 표시
for bar, value in zip(
    bars2,
    mbti_data["비율"]
):
    ax2.text(
        bar.get_width() + 0.3,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.1f}%",
        va="center",
        fontsize=8
    )

plt.tight_layout()

st.pyplot(fig2)


# =========================
# 전체 순위 표
# =========================

with st.expander("📋 국가별 전체 순위 보기"):

    display_data = mbti_data[
        ["Country", "비율"]
    ].copy()

    display_data.insert(
        0,
        "순위",
        range(1, len(display_data) + 1)
    )

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
