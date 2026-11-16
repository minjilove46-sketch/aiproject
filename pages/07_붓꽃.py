
from pathlib import Path
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    # 현재 파이썬 파일의 상위 폴더 경로
    BASE_DIR = Path(__file__).resolve().parent.parent

    # 상위 폴더에 있는 iris.csv 경로
    CSV_PATH = BASE_DIR / "iris.csv"

    # CSV 파일 불러오기
    df = pd.read_csv(CSV_PATH, encoding="cp949")

    # 열 이름의 불필요한 공백 제거
    df.columns = df.columns.str.strip()

    return df

df = load_data()
