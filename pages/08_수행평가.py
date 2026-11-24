
import streamlit as st
import pandas as pd
from pathlib import Path

# -------------------------
# 페이지 설정
# -------------------------
st.set_page_config(
    page_title="알레르기 통합 분석",
    page_icon="🤧",
    layout="wide"
)

st.title("🤧 알레르기 통합 데이터 분석")
st.write("국민건강보험공단 데이터를 활용한 알레르기성 비염 통계 분석")
st.divider()

# -------------------------
# CSV 불러오기
# -------------------------
file_path = Path(__file__).resolve().parent.parent / "allergy_all_data.csv"

try:
    df = pd.read_csv(file_path, encoding="utf-8-sig")
except FileNotFoundError:
    st.error("CSV 파일을 찾을 수 없습니다. GitHub 최상위 폴더를 확인하세요.")
    st.stop()

# 숫자형 데이터 변환
for col in ["진료개시년도", "진료인원", "적용인구", "관내", "관외", "진료환자"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# -------------------------
# 사이드바 검색
# -------------------------
st.sidebar.title("🔍 데이터 검색")

category = st.sidebar.selectbox(
    "분석할 데이터 선택",
    [
        "전체 데이터",
        "진료현황",
        "관외관내",
        "진료과목별"
    ]
)

search_word = st.sidebar.text_input(
    "검색어 입력",
    placeholder="지역, 성별, 연령, 진료과목 등"
)

# 데이터 구분
filtered = df.copy()

if category != "전체 데이터":
    filtered = filtered[
        filtered["데이터구분"] == category
    ]

# -------------------------
# 검색어 적용
# -------------------------
if search_word:
    mask = filtered.astype(str).apply(
        lambda col: col.str.contains(
            search_word,
            case=False,
            na=False,
            regex=False
        )
    ).any(axis=1)

    filtered = filtered[mask]

# -------------------------
# 진료현황 필터
# -------------------------
if category == "진료현황":

    st.sidebar.subheader("📌 상세 조건")

    years = sorted(
        filtered["진료개시년도"].dropna().unique().tolist()
    )

    if years:
        selected_year = st.sidebar.multiselect(
            "연도 선택",
            years,
            default=years
        )
        filtered = filtered[
            filtered["진료개시년도"].isin(selected_year)
        ]

    regions = sorted(
        filtered["수진자시도"].dropna().unique().tolist()
    )

    if regions:
        selected_region = st.sidebar.multiselect(
            "지역 선택",
            regions,
            default=regions
        )
        filtered = filtered[
            filtered["수진자시도"].isin(selected_region)
        ]

    genders = sorted(
        filtered["성별"].dropna().unique().tolist()
    )

    if genders:
        selected_gender = st.sidebar.multiselect(
            "성별 선택",
            genders,
            default=genders
        )
        filtered = filtered[
            filtered["성별"].isin(selected_gender)
        ]

    ages = sorted(
        filtered["연령"].dropna().unique().tolist()
    )

    if ages:
        selected_age = st.sidebar.multiselect(
            "연령 선택",
            ages,
            default=ages
        )
        filtered = filtered[
            filtered["연령"].isin(selected_age)
        ]

# -------------------------
# 관내 관외 필터
# -------------------------
elif category == "관외관내":

    st.sidebar.subheader("📌 상세 조건")

    years = sorted(
        filtered["진료개시년도"].dropna().unique().tolist()
    )

    if years:
        selected_year = st.sidebar.multiselect(
            "연도 선택",
            years,
            default=years
        )
        filtered = filtered[
            filtered["진료개시년도"].isin(selected_year)
        ]

    regions = sorted(
        filtered["수진자시도"].dropna().unique().tolist()
    )

    if regions:
        selected_region = st.sidebar.multiselect(
            "지역 선택",
            regions,
            default=regions
        )
        filtered = filtered[
            filtered["수진자시도"].isin(selected_region)
        ]

# -------------------------
# 진료과목별 필터
# -------------------------
elif category == "진료과목별":

    st.sidebar.subheader("📌 상세 조건")

    years = sorted(
        filtered["진료개시년도"].dropna().unique().tolist()
    )

    if years:
        selected_year = st.sidebar.multiselect(
            "연도 선택",
            years,
            default=years
        )
        filtered = filtered[
            filtered["진료개시년도"].isin(selected_year)
        ]

    subjects = sorted(
        filtered["진료과목"].dropna().unique().tolist()
    )

    if subjects:
        selected_subject = st.sidebar.multiselect(
            "진료과목 선택",
            subjects,
            default=subjects
        )
        filtered = filtered[
            filtered["진료과목"].isin(selected_subject)
        ]

# -------------------------
# 데이터 분석 화면
# -------------------------
st.subheader("📊 분석 결과")

col1, col2, col3 = st.columns(3)

col1.metric(
    "검색된 데이터",
    f"{len(filtered):,}건"
)

if category == "진료현황":
    total = filtered["진료인원"].sum()
    col2.metric("진료인원 합계", f"{total:,.0f}명")

    population = filtered["적용인구"].sum()
    col3.metric("적용인구 합계", f"{population:,.0f}명")

elif category == "관외관내":
    inside = filtered["관내"].sum()
    outside = filtered["관외"].sum()

    col2.metric("관내 환자 합계", f"{inside:,.0f}명")
    col3.metric("관외 환자 합계", f"{outside:,.0f}명")

elif category == "진료과목별":
    total = filtered["진료환자"].sum()
    col2.metric("진료환자 합계", f"{total:,.0f}명")
    col3.metric("진료과목 수", f"{filtered['진료과목'].nunique()}개")

else:
    col2.metric(
        "진료현황 데이터",
        f"{(filtered['데이터구분'] == '진료현황').sum():,}건"
    )
    col3.metric(
        "진료과목 데이터",
        f"{(filtered['데이터구분'] == '진료과목별').sum():,}건"
    )

st.divider()

# -------------------------
# 그래프
# -------------------------
st.subheader("📈 통계 그래프")

if filtered.empty:
    st.warning("검색 결과가 없습니다. 검색 조건을 변경해 주세요.")

elif category == "진료현황":

    graph_type = st.selectbox(
        "그래프 기준 선택",
        ["연도별", "지역별", "성별", "연령별"]
    )

    graph_columns = {
        "연도별": "진료개시년도",
        "지역별": "수진자시도",
        "성별": "성별",
        "연령별": "연령"
    }

    group_col = graph_columns[graph_type]

    chart_df = (
        filtered.groupby(group_col)["진료인원"]
        .sum()
        .reset_index()
    )

    st.bar_chart(
        chart_df,
        x=group_col,
        y="진료인원",
        horizontal=(graph_type != "연도별")
    )

    if graph_type == "연도별":
        line_df = (
            filtered.groupby("진료개시년도")["진료인원"]
            .sum()
            .reset_index()
            .set_index("진료개시년도")
        )

        st.write("📉 연도별 환자 수 변화")
        st.line_chart(line_df)

elif category == "관외관내":

    chart_df = (
        filtered.groupby("수진자시도")[["관내", "관외"]]
        .sum()
    )

    st.bar_chart(chart_df)

elif category == "진료과목별":

    chart_df = (
        filtered.groupby("진료과목")["진료환자"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    st.bar_chart(
        chart_df,
        x="진료과목",
        y="진료환자",
        horizontal=True
    )

else:

    st.info(
        "전체 데이터를 선택했어요. "
        "세부적인 그래프는 왼쪽 메뉴에서 데이터 종류를 선택하면 확인할 수 있습니다."
    )

    summary = (
        filtered.groupby("데이터구분")
        .size()
        .reset_index(name="데이터 수")
    )

    st.bar_chart(
        summary,
        x="데이터구분",
        y="데이터 수"
    )

st.divider()

# -------------------------
# 검색 결과 표
# -------------------------
st.subheader("📋 검색된 전체 데이터")

st.write(f"총 {len(filtered):,}개의 데이터가 검색되었습니다.")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

# -------------------------
# CSV 다운로드
# -------------------------
st.download_button(
    label="📥 검색 결과 다운로드",
    data=filtered.to_csv(index=False).encode("utf-8-sig"),
    file_name="알레르기_검색결과.csv",
    mime="text/csv"
)

st.divider()

st.caption(
    "자료: 국민건강보험공단 알레르기성 비염 관련 통계 | "
    "분석 도구: Pandas"
)
