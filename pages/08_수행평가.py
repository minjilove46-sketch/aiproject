
import streamlit as st
import pandas as pd
from pathlib import Path

# 현재 파이썬 파일 위치 확인
current_dir = Path(__file__).resolve().parent

# CSV 파일을 찾을 위치
search_paths = [
    current_dir / "allergy_all_data.csv",
    current_dir.parent / "allergy_all_data.csv",
    Path.cwd() / "allergy_all_data.csv",
    Path.cwd() / "pages" / "allergy_all_data.csv"
]

# 실제 파일 찾기
file_path = next(
    (p for p in search_paths if p.is_file()),
    None
)

if file_path is None:
    st.error("CSV 파일을 찾을 수 없습니다.")

    st.write("📁 현재 파이썬 파일 위치:")
    st.code(str(current_dir))

    st.write("🔍 확인한 경로:")
    for path in search_paths:
        st.code(str(path))

    st.warning(
        "GitHub에 allergy_all_data.csv 파일을 업로드하고 "
        "Commit changes를 눌러주세요."
    )

    st.stop()

# CSV 불러오기
df = pd.read_csv(file_path, encoding="utf-8-sig")

st.success("✅ CSV 파일을 정상적으로 불러왔습니다!")
