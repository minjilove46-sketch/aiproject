
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

# 페이지 설정
st.set_page_config(
    page_title="붓꽃 품종 예측",
    page_icon="🌸",
    layout="centered"
)

st.title("🌸 붓꽃 품종 예측 프로그램")
st.write("꽃잎의 길이와 너비를 입력하면 붓꽃의 품종을 예측합니다.")

# CSV 파일 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("iris.csv", encoding="cp949")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# 사용할 데이터 선택
X = df[["꽃잎 길이", "꽃잎 너비"]]
y = df["품종"]

# KNN 분류 모델 생성
model = make_pipeline(
    StandardScaler(),
    KNeighborsClassifier(n_neighbors=5)
)

# 모델 학습
model.fit(X, y)

# 데이터 입력
st.subheader("📏 꽃잎 크기 입력")

col1, col2 = st.columns(2)

with col1:
    petal_length = st.number_input(
        "꽃잎 길이 (cm)",
        min_value=float(X["꽃잎 길이"].min()),
        max_value=float(X["꽃잎 길이"].max()),
        value=3.0,
        step=0.1
    )

with col2:
    petal_width = st.number_input(
        "꽃잎 너비 (cm)",
        min_value=float(X["꽃잎 너비"].min()),
        max_value=float(X["꽃잎 너비"].max()),
        value=1.0,
        step=0.1
    )

st.caption(
    "입력 가능 범위: 꽃잎 길이 1.0~6.9cm / "
    "꽃잎 너비 0.1~2.5cm"
)

# 예측 버튼
if st.button("🔍 품종 예측하기", use_container_width=True):

    input_data = pd.DataFrame(
        [[petal_length, petal_width]],
        columns=["꽃잎 길이", "꽃잎 너비"]
    )

    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]

    # 품종 이름
    species_names = {
        "Iris-setosa": "세토사 (Setosa)",
        "Iris-versicolor": "버시컬러 (Versicolor)",
        "Iris-virginica": "버지니카 (Virginica)"
    }

    st.success(
        f"🌸 예측된 품종: {species_names[prediction]}"
    )

    st.write("### 품종별 예측 확률")

    probability_df = pd.DataFrame({
        "품종": [
            species_names[name]
            for name in model.classes_
        ],
        "예측 확률": probabilities
    })

    st.bar_chart(
        probability_df.set_index("품종")
    )

    # 그래프
    st.subheader("📊 입력한 꽃잎 크기 그래프")

    fig, ax = plt.subplots(figsize=(8, 5))

    # 기존 데이터 표시
    ax.scatter(
        X["꽃잎 길이"],
        X["꽃잎 너비"],
        color="lightgray",
        alpha=0.5,
        label="기존 붓꽃 데이터"
    )

    # 사용자가 입력한 값 표시
    ax.scatter(
        petal_length,
        petal_width,
        color="green",
        marker="*",
        s=350,
        edgecolors="black",
        label="입력한 값"
    )

    ax.set_xlabel("꽃잎 길이 (cm)")
    ax.set_ylabel("꽃잎 너비 (cm)")
    ax.set_title("붓꽃 꽃잎 크기 비교")
    ax.legend()
    ax.grid(alpha=0.3)

    st.pyplot(fig)

    st.info(
        "초록색 별은 사용자가 입력한 꽃잎의 크기를 나타냅니다."
    )

# 데이터 정보
with st.expander("📚 데이터 정보 확인하기"):
    st.write("전체 데이터")
    st.dataframe(df)

    st.write("품종별 데이터 개수")
    st.write(df["품종"].value_counts())

    st.write("꽃잎 크기 통계")
    st.write(X.describe())
