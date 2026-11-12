
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="월별 평균기온 예측",
    page_icon="🌡️",
    layout="wide"
)

# 제목
st.title("🌡️ 월별 평균기온 예측 프로그램")
st.write("과거 기온 데이터를 이용해 선형회귀로 미래의 평균기온을 예측해 보세요!")

st.divider()

# CSV 파일 불러오기
@st.cache_data
def load_data():
    data = pd.read_csv("temperature.csv", encoding="cp949")

    # 날짜 데이터 변환
    data["날짜"] = pd.to_datetime(
        data["일시"],
        format="%b-%y",
        errors="coerce"
    )

    # 연도와 월 추출
    data["연도"] = data["날짜"].dt.year
    data["월"] = data["날짜"].dt.month

    # 평균기온 숫자로 변환
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


try:
    df = load_data()

    # 사용자 입력
    st.subheader("📌 예측 조건 선택")

    col1, col2 = st.columns(2)

    with col1:
        month_names = {
            1: "1월", 2: "2월", 3: "3월",
            4: "4월", 5: "5월", 6: "6월",
            7: "7월", 8: "8월", 9: "9월",
            10: "10월", 11: "11월", 12: "12월"
        }

        selected_month = st.selectbox(
            "예측할 월을 선택하세요.",
            list(month_names.keys()),
            format_func=lambda x: month_names[x]
        )

    with col2:
        latest_year = int(df["연도"].max())

        predict_year = st.number_input(
            "예측하고 싶은 연도를 입력하세요.",
            min_value=1900,
            max_value=2100,
            value=latest_year + 1,
            step=1
        )

    # 선택한 월의 데이터 추출
    month_data = df[
        df["월"] == selected_month
    ].copy()

    # 연도순 정렬
    month_data = month_data.sort_values("연도")

    st.divider()

    # 데이터 확인
    st.subheader(
        f"📊 {month_names[selected_month]} 평균기온 데이터"
    )

    if len(month_data) < 2:
        st.warning("선형회귀 분석을 위해 데이터가 2개 이상 필요합니다.")

    else:
        # X와 Y 데이터 설정
        X = month_data[["연도"]]
        y = month_data["평균기온(℃)"]

        # 선형회귀 모델 생성
        model = LinearRegression()

        # 학습
        model.fit(X, y)

        # 예측
        prediction = model.predict(
            pd.DataFrame({"연도": [int(predict_year)]})
        )[0]

        # 회귀계수와 절편
        slope = model.coef_[0]
        intercept = model.intercept_

        # 예측 결과
        st.subheader("🔮 기온 예측 결과")

        result1, result2, result3 = st.columns(3)

        with result1:
            st.metric(
                "예측 연도",
                f"{int(predict_year)}년"
            )

        with result2:
            st.metric(
                "선택한 월",
                month_names[selected_month]
            )

        with result3:
            st.metric(
                "예측 평균기온",
                f"{prediction:.2f} ℃"
            )

        if int(predict_year) > latest_year:
            st.info(
                f"{latest_year}년까지의 데이터를 학습하여 "
                f"{int(predict_year)}년을 예측했습니다."
            )
        else:
            st.info(
                "선택한 연도는 학습 데이터 범위 안에 있습니다. "
                "이 경우 과거 추세를 이용한 추정값으로 확인하세요."
            )

        st.divider()

        # 그래프
        st.subheader("📈 과거 기온 및 예측 기온 그래프")

        # 그래프를 위한 연도 범위
        start_year = int(month_data["연도"].min())
        end_year = max(latest_year, int(predict_year))

        graph_years = pd.DataFrame({
            "연도": range(start_year, end_year + 1)
        })

        graph_predictions = model.predict(graph_years)

        fig, ax = plt.subplots(figsize=(12, 6))

        # 실제 기온
        ax.scatter(
            month_data["연도"],
            month_data["평균기온(℃)"],
            label="Actual Temperature",
            s=45
        )

        # 회귀 직선
        ax.plot(
            graph_years["연도"],
            graph_predictions,
            label="Linear Regression",
            linewidth=2
        )

        # 예측 기온
        ax.scatter(
            [int(predict_year)],
            [prediction],
            color="red",
            s=130,
            marker="*",
            label="Predicted Temperature",
            zorder=5
        )

        # 예측값 표시
        ax.annotate(
            f"{prediction:.2f} C",
            (int(predict_year), prediction),
            xytext=(8, 12),
            textcoords="offset points"
        )

        ax.set_title(
            f"Average Temperature in {month_names[selected_month]}"
        )
        ax.set_xlabel("Year")
        ax.set_ylabel("Average Temperature (C)")
        ax.legend()
        ax.grid(True, alpha=0.3)

        st.pyplot(fig)
        plt.close(fig)

        st.divider()

        # 과거 데이터 표
        st.subheader("📋 과거 기온 데이터 전체")

        display_data = month_data[
            ["연도", "평균기온(℃)"]
        ].copy()

        display_data.columns = [
            "연도",
            "평균기온(℃)"
        ]

        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # 선형회귀 알고리즘 설명
        st.subheader("🧠 선형회귀 알고리즘 작동 원리")

        st.write("""
        선형회귀는 과거의 데이터를 분석하여 두 변수 사이의
        관계를 직선으로 나타내고, 이를 이용해 새로운 값을
        예측하는 머신러닝 알고리즘입니다.
        """)

        st.markdown("### ① 데이터 학습")

        st.write("""
        과거의 연도를 X값으로, 평균기온을 Y값으로 설정합니다.
        선택한 월에 해당하는 모든 과거 데이터를 학습에 사용합니다.
        """)

        st.markdown("### ② 최적의 직선 찾기")

        st.write("""
        데이터의 점들과 가장 잘 맞는 직선을 찾습니다.
        이때 실제 기온과 직선이 예측한 기온의 차이를
        제곱하여 모두 더한 값이 가장 작아지도록 계산합니다.
        """)

        st.markdown("### ③ 예측 공식")

        st.latex(r"\hat{y} = b_0 + b_1x")

        st.write(f"""
        - X: 연도
        - ŷ: 예측 평균기온
        - b₀: 절편 ({intercept:.4f})
        - b₁: 기울기 ({slope:.4f})
        """)

        st.markdown("### ④ 예측 결과 계산")

        st.write(f"""
        학습한 직선에 {int(predict_year)}년을 대입하면
        해당 연도의 평균기온을 예측할 수 있습니다.
        """)

        st.latex(
            rf"\hat{{y}} = {intercept:.4f} + "
            rf"({slope:.4f} \times {int(predict_year)})"
        )

        st.success(
            f"최종 예측 평균기온: {prediction:.2f} ℃"
        )

        st.divider()

        st.caption(
            "※ 이 결과는 과거 데이터의 선형적인 추세를 바탕으로 "
            "계산한 예측값이며, 실제 기온과 다를 수 있습니다."
        )

except FileNotFoundError:
    st.error(
        "temperature.csv 파일을 찾을 수 없습니다. "
        "app.py와 같은 폴더에 CSV 파일을 넣어주세요."
    )

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
