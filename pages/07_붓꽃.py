
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# --------------------------------
# 1. 페이지 설정
# --------------------------------
st.set_page_config(
    page_title="붓꽃 품종 예측",
    page_icon="🌸",
    layout="centered"
)

st.title("🌸 붓꽃 품종 예측 프로그램")
st.write(
    "꽃의 크기를 입력하고 다양한 분류 알고리즘으로 "
    "붓꽃의 품종을 예측해 보세요!"
)

# --------------------------------
# 2. 데이터 불러오기
# --------------------------------
@st.cache_data
def load_data():

    BASE_DIR = Path(__file__).resolve().parent.parent
    CSV_PATH = BASE_DIR / "iris.csv"

    if not CSV_PATH.exists():
        st.error(f"CSV 파일을 찾을 수 없습니다: {CSV_PATH}")
        st.stop()

    try:
        df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(CSV_PATH, encoding="cp949")
        except UnicodeDecodeError:
            df = pd.read_csv(CSV_PATH, encoding="euc-kr")

    df.columns = df.columns.str.strip()

    return df


df = load_data()

# 사용할 속성
features = [
    "꽃받침 길이",
    "꽃받침 너비",
    "꽃잎 길이",
    "꽃잎 너비"
]

required_columns = features + ["품종"]

if not all(col in df.columns for col in required_columns):
    st.error("CSV 파일의 열 이름을 확인해 주세요.")
    st.write(df.columns.tolist())
    st.stop()

# 데이터 정리
data = df[required_columns].copy()

for col in features:
    data[col] = pd.to_numeric(data[col], errors="coerce")

data = data.dropna()

# 품종 이름
species_names = {
    "Iris-setosa": "세토사 (Setosa)",
    "Iris-versicolor": "버시컬러 (Versicolor)",
    "Iris-virginica": "버지니카 (Virginica)"
}

# --------------------------------
# 3. 알고리즘 설명
# --------------------------------
algorithm_info = {
    "KNN": """
    **KNN (K-최근접 이웃)**

    새로운 데이터와 기존 데이터 사이의 거리를 계산합니다.
    가장 가까운 5개의 데이터를 찾고 가장 많이 나타난
    품종을 예측합니다.

    쉽게 말하면 나와 가장 비슷한 꽃 5개를 찾아
    어떤 품종인지 알아보는 방법입니다.
    """,

    "Decision Tree": """
    **Decision Tree (의사결정나무)**

    데이터를 여러 가지 조건으로 나누면서 품종을 분류합니다.
    꽃받침이나 꽃잎의 크기를 차례대로 판단하여
    최종 품종을 예측합니다.

    쉽게 말하면 질문에 하나씩 답하면서
    정답을 찾아가는 스무고개와 비슷한 방법입니다.
    """,

    "Random Forest": """
    **Random Forest (랜덤 포레스트)**

    여러 개의 의사결정나무를 만들어 각각 품종을 예측합니다.
    여러 나무가 예측한 결과를 모아
    가장 많은 표를 받은 품종을 최종 결과로 결정합니다.

    쉽게 말하면 여러 사람이 의견을 내고
    가장 많은 사람이 선택한 답을 결정하는 방법입니다.
    """
}

# --------------------------------
# 4. 알고리즘 생성 함수
# --------------------------------
def create_model(name):

    if name == "KNN":
        return make_pipeline(
            StandardScaler(),
            KNeighborsClassifier(n_neighbors=5)
        )

    elif name == "Decision Tree":
        return DecisionTreeClassifier(
            max_depth=4,
            random_state=42
        )

    else:
        return RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )


# --------------------------------
# 5. 예측 프로그램 함수
# --------------------------------
def prediction_page(feature_cols, page_key):

    # 알고리즘 선택
    st.subheader("🤖 분류 알고리즘 선택")

    algorithm = st.selectbox(
        "사용할 알고리즘을 선택하세요.",
        ["KNN", "Decision Tree", "Random Forest"],
        key=f"algorithm_{page_key}"
    )

    # 선택한 속성 데이터
    X = data[feature_cols]
    y = data["품종"]

    # 모델 생성 및 학습
    model = create_model(algorithm)
    model.fit(X, y)

    # --------------------------------
    # 6. 사용자 입력
    # --------------------------------
    st.subheader("📏 측정값 입력")

    col1, col2 = st.columns(2)

    input_values = []

    for i, feature in enumerate(feature_cols):

        min_value = float(X[feature].min())
        max_value = float(X[feature].max())

        if feature == "꽃잎 길이":
            default_value = 3.0
        elif feature == "꽃잎 너비":
            default_value = 1.0
        elif feature == "꽃받침 길이":
            default_value = 5.8
        else:
            default_value = 3.0

        default_value = max(
            min_value,
            min(default_value, max_value)
        )

        with (col1 if i == 0 else col2):

            value = st.number_input(
                f"{feature} (cm)",
                min_value=min_value,
                max_value=max_value,
                value=default_value,
                step=0.1,
                key=f"input_{page_key}_{i}"
            )

        input_values.append(value)

    st.info(
        f"첫 번째 속성 범위: "
        f"{X[feature_cols[0]].min():.1f} ~ "
        f"{X[feature_cols[0]].max():.1f} cm\n\n"
        f"두 번째 속성 범위: "
        f"{X[feature_cols[1]].min():.1f} ~ "
        f"{X[feature_cols[1]].max():.1f} cm"
    )

    # --------------------------------
    # 7. 예측 버튼
    # --------------------------------
    if st.button(
        "🔍 품종 예측하기",
        use_container_width=True,
        key=f"predict_{page_key}"
    ):

        input_data = pd.DataFrame(
            [input_values],
            columns=feature_cols
        )

        prediction = model.predict(input_data)[0]

        probabilities = model.predict_proba(input_data)[0]

        predicted_name = species_names.get(
            prediction, str(prediction)
        )

        st.success(
            f"🌸 예측된 붓꽃 품종: {predicted_name}"
        )

        st.caption(f"사용한 알고리즘: {algorithm}")

        # --------------------------------
        # 8. 예측 확률
        # --------------------------------
        st.subheader("📊 품종별 예측 확률")

        probability_df = pd.DataFrame({
            "품종": [
                species_names.get(name, str(name))
                for name in model.classes_
            ],
            "예측 확률": probabilities * 100
        })

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

        # --------------------------------
        # 9. 그래프
        # --------------------------------
        st.subheader("🌱 입력한 속성 그래프")

        fig, ax = plt.subplots(figsize=(8, 5))

        # 기존 붓꽃 데이터
        ax.scatter(
            X[feature_cols[0]],
            X[feature_cols[1]],
            color="lightgray",
            alpha=0.5,
            label="Existing Data"
        )

        # 사용자 입력값
        ax.scatter(
            input_values[0],
            input_values[1],
            color="green",
            marker="*",
            s=350,
            edgecolors="black",
            label="Your Input"
        )

        ax.set_xlabel(f"{feature_cols[0]} (cm)")
        ax.set_ylabel(f"{feature_cols[1]} (cm)")
        ax.set_title("Iris Data Graph")

        ax.legend()
        ax.grid(alpha=0.3)

        st.pyplot(fig)

        st.caption(
            "⭐ 초록색 별은 사용자가 입력한 값입니다."
        )

        # --------------------------------
        # 10. 알고리즘 작동 원리
        # --------------------------------
        st.divider()

        st.subheader("📚 알고리즘 작동 원리")

        with st.expander(
            "선택한 알고리즘의 작동 원리 확인하기",
            expanded=True
        ):

            st.markdown(algorithm_info[algorithm])

        # --------------------------------
        # 11. 사용한 속성 정보
        # --------------------------------
        st.subheader("💡 이번 예측에 사용한 속성")

        for feature, value in zip(feature_cols, input_values):
            st.write(f"- **{feature}:** {value:.1f} cm")


# --------------------------------
# 12. 탭 만들기
# --------------------------------
tab1, tab2 = st.tabs([
    "🌸 꽃잎으로 예측하기",
    "🔍 원하는 속성으로 예측하기"
])

# 첫 번째 탭
with tab1:

    st.header("꽃잎 크기로 품종 예측")

    st.write(
        "기존 방식대로 꽃잎 길이와 꽃잎 너비를 "
        "이용하여 품종을 예측합니다."
    )

    prediction_page(
        ["꽃잎 길이", "꽃잎 너비"],
        "petal"
    )


# 두 번째 탭
with tab2:

    st.header("원하는 속성 2개로 품종 예측")

    st.write(
        "4가지 속성 중 원하는 2가지를 선택하여 "
        "새로운 방식으로 품종을 예측해 보세요."
    )

    st.subheader("🔎 사용할 속성 선택")

    col1, col2 = st.columns(2)

    with col1:

        first_feature = st.selectbox(
            "첫 번째 속성",
            features,
            index=0,
            key="custom_feature1"
        )

    # 첫 번째 속성과 중복되지 않게 설정
    second_options = [
        feature for feature in features
        if feature != first_feature
    ]

    with col2:

        default_second = (
            "꽃받침 너비"
            if "꽃받침 너비" in second_options
            else second_options[0]
        )

        second_feature = st.selectbox(
            "두 번째 속성",
            second_options,
            index=second_options.index(default_second),
            key="custom_feature2"
        )

    st.success(
        f"선택한 속성: {first_feature} + {second_feature}"
    )

    st.divider()

    # 선택한 두 속성으로 예측
    prediction_page(
        [first_feature, second_feature],
        "custom"
    )


# --------------------------------
# 13. 데이터 정보
# --------------------------------
with st.expander("📖 데이터 정보 확인하기"):

    st.write("### 전체 데이터")
    st.dataframe(df, use_container_width=True)

    st.write("### 품종별 데이터 개수")
    st.write(data["품종"].value_counts())

    st.write("### 전체 속성 통계")
    st.dataframe(data[features].describe())

    st.write("### 사용한 알고리즘")
    st.write("""
    1. KNN - 가까운 데이터 비교
    2. Decision Tree - 조건에 따라 분류
    3. Random Forest - 여러 결정 트리의 결과 종합
    """)
