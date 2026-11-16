
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="붓꽃 품종 예측",
    page_icon="🌸",
    layout="centered"
)

# 제목
st.title("🌸 붓꽃 품종 예측 프로그램")
st.write(
    "꽃잎의 길이와 너비를 입력하면 "
    "붓꽃의 품종을 예측합니다."
)

# CSV 파일 불러오기
@st.cache_data
def load_data():

    # 현재 파이썬 파일의 상위 폴더 경로
    BASE_DIR = Path(__file__).resolve().parent.parent

    # CSV 파일 경로
    CSV_PATH = BASE_DIR / "iris.csv"

    # 파일 존재 여부 확인
    if not CSV_PATH.exists():
        st.error(f"CSV 파일을 찾을 수 없습니다: {CSV_PATH}")
        st.stop()

    # CSV 파일 읽기
    # 여러 인코딩에 대응
    try:
        df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(CSV_PATH, encoding="cp949")
        except UnicodeDecodeError:
            df = pd.read_csv(CSV_PATH, encoding="euc-kr")

    # 열 이름 공백 제거
    df.columns = df.columns.str.strip()

    return df


df = load_data()

# 필요한 열 확인
required_columns = ["꽃잎 길이", "꽃잎 너비", "품종"]

if not all(col in df.columns for col in required_columns):
    st.error(
        "CSV 파일의 열 이름을 확인해주세요. "
        "필요한 열: 꽃잎 길이, 꽃잎 너비, 품종"
    )
    st.write("현재 CSV 열 이름:", df.columns.tolist())
    st.stop()

# 데이터 선택
X = df[["꽃잎 길이", "꽃잎 너비"]]
y = df["품종"]

# 결측치 제거
valid_data = pd.concat([X, y], axis=1).dropna()

X = valid_data[["꽃잎 길이", "꽃잎 너비"]]
y = valid_data["품종"]

# KNN 모델 생성
model = make_pipeline(
    StandardScaler(),
    KNeighborsClassifier(n_neighbors=5)
)

# 모델 학습
model.fit(X, y)

# 입력 화면
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

# 입력 가능 범위
st.info(
    f"꽃잎 길이: {X['꽃잎 길이'].min():.1f} ~ "
    f"{X['꽃잎 길이'].max():.1f} cm\n\n"
    f"꽃잎 너비: {X['꽃잎 너비'].min():.1f} ~ "
    f"{X['꽃잎 너비'].max():.1f} cm"
)

# 예측 버튼
if st.button("🔍 품종 예측하기", use_container_width=True):

    input_data = pd.DataFrame(
        [[petal_length, petal_width]],
        columns=["꽃잎 길이", "꽃잎 너비"]
    )

    # 품종 예측
    prediction = model.predict(input_data)[0]

    # 예측 확률
    probabilities = model.predict_proba(input_data)[0]

    # 품종 이름 변환
    species_names = {
        "Iris-setosa": "세토사 (Setosa)",
        "Iris-versicolor": "버시컬러 (Versicolor)",
        "Iris-virginica": "버지니카 (Virginica)"
    }

    predicted_name = species_names.get(
        prediction, str(prediction)
    )

    # 예측 결과
    st.success(
        f"🌸 예측된 붓꽃 품종: {predicted_name}"
    )

    # 확률 표시
    st.subheader("📊 품종별 예측 확률")

    probability_df = pd.DataFrame({
        "품종": [
            species_names.get(name, str(name))
            for name in model.classes_
        ],
        "예측 확률": probabilities
    })

    probability_df["예측 확률"] *= 100

    st.bar_chart(
        probability_df.set_index("품종")
    )

    st.dataframe(
        probability_df.style.format(
            {"예측 확률": "{:.1f}%"}
        ),
        use_container_width=True,
        hide_index=True
    )

    # 그래프
    st.subheader("🌱 꽃잎 크기 그래프")

    fig, ax = plt.subplots(figsize=(8, 5))

    # 기존 데이터
    ax.scatter(
        X["꽃잎 길이"],
        X["꽃잎 너비"],
        color="lightgray",
        alpha=0.5,
        label="Existing Data"
    )

    # 사용자가 입력한 값
    ax.scatter(
        petal_length,
        petal_width,
        color="green",
        marker="*",
        s=350,
        edgecolors="black",
        label="Your Input"
    )

    ax.set_xlabel("Petal Length (cm)")
    ax.set_ylabel("Petal Width (cm)")
    ax.set_title("Iris Petal Size")
    ax.legend()
    ax.grid(alpha=0.3)

    st.pyplot(fig)

    st.info(
        "초록색 별은 사용자가 입력한 꽃잎의 크기입니다."
    )

# 데이터 정보
with st.expander("📚 데이터 정보 확인하기"):

    st.write("### 전체 데이터")
    st.dataframe(df, use_container_width=True)

    st.write("### 품종별 데이터 개수")
    st.write(y.value_counts())

    st.write("### 꽃잎 크기 통계")
    st.dataframe(X.describe())

    st.write("### 사용한 알고리즘")
    st.write(
        "KNN (K-최근접 이웃 알고리즘)\n\n"
        "가까운 데이터 5개의 품종을 비교하여 "
        "새로운 붓꽃의 품종을 예측합니다."
    )
