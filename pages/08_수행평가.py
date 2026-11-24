
import io

import pandas as pd
import streamlit as st


# -------------------- 기본 설정 --------------------

st.set_page_config(
    page_title="알레르기성 비염 통계 분석",
    page_icon="🤧",
    layout="wide"
)


# -------------------- 데이터 불러오기 --------------------

@st.cache_data
def load_data(file_bytes):

    excel_data = pd.read_excel(
        io.BytesIO(file_bytes),
        sheet_name=None
    )

    data_list = []

    sheet_names = {
        "진료현황": "진료현황",
        "(추가) 관외,관내": "관외관내",
        "(추가) 진료과목별": "진료과목별"
    }

    for sheet_name, data_type in sheet_names.items():

        if sheet_name in excel_data:

            temp = excel_data[sheet_name].copy()

            temp["데이터구분"] = data_type

            data_list.append(temp)

    if not data_list:
        return pd.DataFrame()

    result = pd.concat(
        data_list,
        ignore_index=True,
        sort=False
    )

    return result


# -------------------- 화면 제목 --------------------

st.title("🤧 알레르기성 비염 통계 분석")

st.caption(
    "국민건강보험공단 알레르기성 비염 관련 상병코드 그룹별 환자 수 자료"
)

st.info(
    "이 자료는 알레르기성 비염 관련 통계입니다. "
    "식품 알레르기나 아토피 등 모든 알레르기 질환을 포함하지는 않습니다."
)


# -------------------- 엑셀 파일 업로드 --------------------

st.subheader("📂 데이터 파일 불러오기")

uploaded_file = st.file_uploader(
    "국민건강보험공단 원본 엑셀 파일을 업로드하세요.",
    type=["xlsx"]
)

if uploaded_file is None:

    st.warning(
        "분석을 시작하려면 원본 엑셀 파일을 업로드해 주세요."
    )

    st.stop()


try:

    df = load_data(uploaded_file.getvalue())

except ImportError:

    st.error(
        "엑셀 파일을 읽기 위한 openpyxl 라이브러리가 필요합니다."
    )

    st.stop()

except Exception as e:

    st.error(f"파일을 불러오는 중 오류가 발생했습니다: {e}")

    st.stop()


if df.empty:

    st.error("엑셀 파일에서 분석할 데이터를 찾을 수 없습니다.")

    st.stop()


st.success(
    f"데이터 불러오기 완료! 총 {len(df):,}개의 데이터가 있습니다."
)


# -------------------- 사이드바 검색 --------------------

st.sidebar.header("🔎 데이터 검색")

category_labels = {
    "전체 데이터": None,
    "진료현황": "진료현황",
    "관외·관내": "관외관내",
    "진료과목별": "진료과목별"
}

selected_category = st.sidebar.selectbox(
    "분석할 데이터 종류",
    list(category_labels.keys())
)


filtered = df.copy()


# 데이터 종류 선택

if category_labels[selected_category] is not None:

    filtered = filtered[
        filtered["데이터구분"] == category_labels[selected_category]
    ].copy()


# 내용 검색

search_word = st.sidebar.text_input(
    "내용 검색",
    placeholder="예: 서울특별시, 남자, 이비인후과"
)

if search_word.strip():

    search_mask = filtered.astype(str).apply(
        lambda column: column.str.contains(
            search_word.strip(),
            case=False,
            na=False,
            regex=False
        )
    ).any(axis=1)

    filtered = filtered[search_mask].copy()


# -------------------- 세부 필터 --------------------

filter_settings = [
    ("진료개시년도", "연도 선택"),
    ("수진자시도", "지역 선택"),
    ("성별", "성별 선택"),
    ("연령", "연령 선택"),
    ("진료과목", "진료과목 선택")
]


for column_name, label in filter_settings:

    if (
        column_name in filtered.columns
        and filtered[column_name].notna().any()
    ):

        values = filtered[column_name].dropna().unique().tolist()

        values = sorted(
            values,
            key=lambda value: str(value)
        )

        selected_values = st.sidebar.multiselect(
            label,
            options=values,
            default=values,
            key=f"filter_{column_name}_{selected_category}"
        )

        filtered = filtered[
            filtered[column_name].isin(selected_values)
        ].copy()


# -------------------- 요약 정보 --------------------

st.divider()

st.subheader("📊 검색 결과 요약")

col1, col2, col3 = st.columns(3)

col1.metric(
    "검색된 데이터",
    f"{len(filtered):,}건"
)

if not filtered.empty:

    col2.metric(
        "데이터 종류",
        f"{filtered['데이터구분'].nunique()}개"
    )

else:

    col2.metric("데이터 종류", "0개")


# -------------------- 환자 수 항목 선택 --------------------

st.divider()

st.subheader("📈 환자 수 분석")

numeric_columns = [
    "진료인원",
    "적용인구",
    "관내",
    "관외",
    "진료환자"
]

available_columns = [
    column
    for column in numeric_columns
    if column in filtered.columns
    and filtered[column].notna().any()
]


if available_columns:

    selected_measure = st.selectbox(
        "분석할 항목 선택",
        available_columns
    )

    filtered[selected_measure] = pd.to_numeric(
        filtered[selected_measure],
        errors="coerce"
    )

    total_value = filtered[selected_measure].sum()

    col3.metric(
        f"{selected_measure} 합계",
        f"{total_value:,.0f}명"
    )

else:

    selected_measure = None

    col3.metric("환자 수 합계", "-")


# -------------------- 그래프 --------------------

if filtered.empty:

    st.warning(
        "검색 결과가 없습니다. 검색어나 필터를 변경해 주세요."
    )

elif selected_measure is not None:

    group_candidates = [
        column
        for column in [
            "진료개시년도",
            "수진자시도",
            "성별",
            "연령",
            "진료과목"
        ]
        if column in filtered.columns
        and filtered[column].nunique(dropna=True) > 1
    ]

    if group_candidates:

        default_group = (
            "진료개시년도"
            if "진료개시년도" in group_candidates
            else group_candidates[0]
        )

        selected_group = st.selectbox(
            "그래프 분류 기준",
            group_candidates,
            index=group_candidates.index(default_group)
        )

        chart_data = filtered.copy()

        chart_data[selected_measure] = pd.to_numeric(
            chart_data[selected_measure],
            errors="coerce"
        )

        chart_summary = (
            chart_data
            .dropna(subset=[selected_measure])
            .groupby(selected_group)[selected_measure]
            .sum()
            .reset_index()
        )

        chart_summary[selected_group] = (
            chart_summary[selected_group].astype(str)
        )

        if selected_group == "진료개시년도":

            chart_summary = chart_summary.sort_values(
                selected_group
            )

        st.subheader("📊 막대그래프")

        st.bar_chart(
            chart_summary,
            x=selected_group,
            y=selected_measure,
            use_container_width=True
        )

        if selected_group == "진료개시년도":

            st.subheader("📉 연도별 변화")

            line_data = chart_summary.set_index(
                selected_group
            )[[selected_measure]]

            st.line_chart(
                line_data,
                use_container_width=True
            )

    else:

        st.info(
            "현재 검색 결과에는 비교할 분류 항목이 충분하지 않습니다."
        )


# -------------------- 데이터 표 --------------------

st.divider()

st.subheader("📋 검색된 데이터 전체 보기")

st.write(
    f"검색 결과: **{len(filtered):,}건**"
)

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)


# -------------------- CSV 다운로드 --------------------

csv_data = filtered.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    label="📥 검색 결과 CSV 다운로드",
    data=csv_data,
    file_name="알레르기성_비염_검색결과.csv",
    mime="text/csv"
)


# -------------------- 출처 --------------------

st.caption(
    "분석 도구: Pandas | "
    "데이터 출처: 국민건강보험공단 제공 엑셀 자료"
)
