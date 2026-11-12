
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from pathlib import Path

# ---------------------------------
# 1. 페이지 설정
# ---------------------------------
st.set_page_config(
    page_title="월별 평균기온 예측",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월별 평균기온 예측 프로그램")
st.write(
    "과거 기온 데이터를 이용하여 "
    "다양한 회귀 알고리즘으로 미래의 평균기온을 예측해 보세요!"
)

st.divider()

# ---------------------------------
# 2. CSV 파일 경로 설정
# ---------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "temperature.csv"


# ---------------------------------
# 3. 데이터 불러오기
# ---------------------------------
@st.cache_data
def load_data():
    data = pd.read_csv(
        CSV_PATH,
        encoding="cp949"
    )

    # 날짜 변환
    data["날짜"] = pd.to_datetime(
        data["일시"],
        format="%b-%y",
        errors="coerce"
    )

    # 연도와 월 추출
    data["연도"] = data["날짜"].dt.year
    data["월"] = data["날짜"].dt.month

    # 평균기온 숫자 변환
    data["평균기온(℃)"] = pd.to_numeric(
        data["평균기온(℃)"],
        errors="coerce"
    )

    # 결측치 제거
    data = data.dropna(
        subset=["연도", "월", "평균기온(℃)"]
    )

    data["연도"] = data["연도"].astype(int)
    data["월"] = data["월"].astype(int)

    return data


# ---------------------------------
# 4. 월 이름
# ---------------------------------
month_names = {
    1: "1월", 2: "2월", 3: "3월",
    4: "4월", 5: "5월", 6: "6월",
    7: "7월", 8: "8월", 9: "9월",
    10: "10월", 11: "11월", 12: "12월"
}


# ---------------------------------
# 5. 알고리즘 설명
# ---------------------------------
algorithm_info = {
    "선형회귀": """
    선형회귀는 과거 연도와 평균기온 사이의 관계를
    직선으로 나타내는 알고리즘입니다.

    데이터와 가장 잘 맞는 직선을 찾아
    미래의 평균기온을 예측합니다.

    공식: ŷ = b₀ + b₁x
    """,

    "랜덤 포레스트 회귀": """
    랜덤 포레스트는 여러 개의 결정트리를 만들어
    각각 예측한 결과를 평균 내는 알고리즘입니다.

    여러 트리의 결과를 종합하기 때문에
    하나의 결정트리보다 예측 결과가 안정적일 수 있습니다.

    작동 방식:
    여러 결정트리 생성 → 각각 예측 → 예측값 평균
    """,

    "결정트리 회귀": """
    결정트리 회귀는 데이터를 여러 구간으로 나누어
    각 구간에 해당하는 평균기온을 예측하는 알고리즘입니다.

    나무의 가지처럼 데이터를 분류하여
    조건에 맞는 결과를 찾아냅니다.

    작동 방식:
    데이터 분할 → 구간별 평균 계산 → 기온 예측
    """
}


# ---------------------------------
# 6. 프로그램 실행
# ---------------------------------
try:
    df = load_data()

    if df.empty:
        st.error("CSV 파일에 분석할 수 있는 기온 데이터가 없습니다.")
        st.stop()

    latest_year = int(df["연도"].max())

    # 사용자 입력
    st.subheader("📌 예측 조건 선택")

    col1, col2 = st.columns(2)

    with col1:
        selected_month = st.selectbox(
            "예측할 월을 선택하세요.",
            list(month_names.keys()),
            format_func=lambda x: month_names[x]
        )

    with col2:
        predict_year = st.number_input(
            "예측하고 싶은 연도를 입력하세요.",
            min_value=1900,
            max_value=2100,
            value=latest_year + 1,
            step=1
        )

    # 선택한 월 데이터
    month_data = df[
        df["월"] == selected_month
    ].copy()

    month_data = month_data.sort_values("연도")

    st.divider()

    # ---------------------------------
    # 7. 알고리즘 선택
    # ---------------------------------
    st.subheader("🤖 회귀 알고리즘 선택")

    selected_algorithm = st.selectbox(
        "사용할 예측 알고리즘을 선택하세요.",
        [
            "선형회귀",
            "랜덤 포레스트 회귀",
            "결정트리 회귀"
        ]
    )

    st.info(
        f"현재 선택한 알고리즘: {selected_algorithm}"
    )

    if len(month_data) < 2:
        st.warning(
            "회귀 분석을 위해서는 데이터가 2개 이상 필요합니다."
        )
        st.stop()

    # ---------------------------------
    # 8. 학습 데이터 준비
    # ---------------------------------
    X = month_data[["연도"]]
    y = month_data["평균기온(℃)"]

    # ---------------------------------
    # 9. 회귀 모델 생성
    # ---------------------------------
    models = {
        "선형회귀": LinearRegression(),

        "랜덤 포레스트 회귀": RandomForestRegressor(
            n_estimators=200,
            max_depth=5,
            random_state=42
        ),

        "결정트리 회귀": DecisionTreeRegressor(
            max_depth=4,
            random_state=42
        )
    }

    # 모든 알고리즘 학습
    for name, model in models.items():
        model.fit(X, y)

    # 선택한 알고리즘
    selected_model = models[selected_algorithm]

    # 예측 연도
    prediction_input = pd.DataFrame({
        "연도": [int(predict_year)]
    })

    prediction = selected_model.predict(
        prediction_input
    )[0]

    # ---------------------------------
    # 10. 세 알고리즘 예측값 비교
    # ---------------------------------
    predictions = {}

    for name, model in models.items():
        predictions[name] = model.predict(
            prediction_input
        )[0]

    st.divider()

    st.subheader("🔮 기온 예측 결과")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "예측 연도",
        f"{int(predict_year)}년"
    )

    col2.metric(
        "선택한 월",
        month_names[selected_month]
    )

    col3.metric(
        "선택한 알고리즘의 예측 기온",
        f"{prediction:.2f} ℃"
    )

    st.success(
        f"{selected_algorithm}으로 예측한 "
        f"{int(predict_year)}년 {month_names[selected_month]} "
        f"평균기온은 {prediction:.2f}℃입니다."
    )

    if int(predict_year) > latest_year:
        st.caption(
            f"{latest_year}년까지의 과거 데이터를 학습하여 예측했습니다."
        )
    else:
        st.caption(
            "과거 데이터 범위 안의 연도를 선택했습니다. "
            "해당 연도의 추정값을 확인할 수 있습니다."
        )

    # ---------------------------------
    # 11. 세 알고리즘 결과 비교표
    # ---------------------------------
    st.divider()

    st.subheader("📊 알고리즘별 예측 결과 비교")

    comparison = pd.DataFrame({
        "회귀 알고리즘": list(predictions.keys()),
        "예측 평균기온(℃)": [
            round(value, 2)
            for value in predictions.values()
        ]
    })

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )

    st.write(
        "알고리즘마다 데이터를 학습하고 예측하는 방식이 다르기 때문에 "
        "같은 연도를 입력해도 예측 기온이 달라질 수 있습니다."
    )

    # ---------------------------------
    # 12. 그래프
    # ---------------------------------
    st.divider()

    st.subheader("📈 세 가지 알고리즘 예측 그래프")

    start_year = int(month_data["연도"].min())
    end_year = max(
        latest_year,
        int(predict_year)
    )

    graph_years = pd.DataFrame({
        "연도": range(start_year, end_year + 1)
    })

    fig, ax = plt.subplots(figsize=(13, 6))

    # 실제 기온 데이터
    ax.scatter(
        month_data["연도"],
        month_data["평균기온(℃)"],
        color="black",
        s=45,
        label="Actual Temperature",
        zorder=5
    )

    # 알고리즘별 예측선
    for name, model in models.items():

        graph_predictions = model.predict(
            graph_years
        )

        # 선택한 알고리즘은 굵게 표시
        if name == selected_algorithm:
            ax.plot(
                graph_years["연도"],
                graph_predictions,
                linewidth=3,
                label=f"{name} (Selected)"
            )
        else:
            ax.plot(
                graph_years["연도"],
                graph_predictions,
                linewidth=1.8,
                linestyle="--",
                label=name
            )

    # 선택한 알고리즘의 예측값 표시
    ax.scatter(
        [int(predict_year)],
        [prediction],
        color="red",
        s=150,
        marker="*",
        label="Selected Prediction",
        zorder=10
    )

    ax.annotate(
        f"{prediction:.2f} C",
        (int(predict_year), prediction),
        xytext=(8, 12),
        textcoords="offset points"
    )

    ax.set_title(
        f"{month_names[selected_month]} Average Temperature Prediction"
    )

    ax.set_xlabel("Year")
    ax.set_ylabel("Average Temperature (C)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    st.pyplot(fig)
    plt.close(fig)

    # ---------------------------------
    # 13. 과거 기온 데이터
    # ---------------------------------
    st.divider()

    st.subheader("📋 과거 평균기온 데이터 전체")

    display_data = month_data[
        ["연도", "평균기온(℃)"]
    ].copy()

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )

    # ---------------------------------
    # 14. 알고리즘 설명
    # ---------------------------------
    st.divider()

    st.subheader("🧠 선택한 회귀 알고리즘 작동 원리")

    st.markdown(
        f"### {selected_algorithm}"
    )

    st.write(
        algorithm_info[selected_algorithm]
    )

    st.markdown("### 실제 예측 결과")

    st.write(
        f"선택한 알고리즘은 {int(predict_year)}년 "
        f"{month_names[selected_month]}의 평균기온을 "
        f"{prediction:.2f}℃로 예측했습니다."
    )

    st.markdown("### 세 알고리즘의 차이")

    st.write("""
    - 선형회귀: 전체 데이터의 직선적인 추세를 분석합니다.
    - 랜덤 포레스트: 여러 결정트리의 예측값을 평균 냅니다.
    - 결정트리: 데이터를 여러 구간으로 나누어 예측합니다.
    """)

    st.warning("""
    참고: 랜덤 포레스트와 결정트리는 학습 데이터의 범위를
    벗어난 미래 연도를 예측할 때 새로운 추세를 만들어 외삽하지 못합니다.
    따라서 미래 예측값이 마지막 학습 구간의 값과 비슷하게 나타날 수 있습니다.
    """)

    st.divider()

    st.caption(
        "※ 본 프로그램은 과거 평균기온 데이터를 이용한 "
        "머신러닝 예측 프로그램이며 실제 기온과 차이가 있을 수 있습니다."
    )

except FileNotFoundError:
    st.error(
        f"temperature.csv 파일을 찾을 수 없습니다.\n"
        f"파일 경로: {CSV_PATH}"
    )

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
