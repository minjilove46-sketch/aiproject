import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="MBTI 진로 추천",
    page_icon="🧭",
    layout="centered"
)

# -----------------------------
# MBTI 진로 데이터
# -----------------------------
career_data = {
    "ISTJ": [
        {
            "career": "회계사 📊",
            "department": "회계학과, 경영학과, 세무회계학과",
            "personality": "꼼꼼하고 책임감이 강하며 정확하게 일하는 성격",
            "salary": "평균 연봉 약 5,000만~7,000만 원"
        },
        {
            "career": "공무원 🏢",
            "department": "행정학과, 법학과, 사회학과",
            "personality": "책임감이 강하고 규칙을 잘 지키며 꾸준한 성격",
            "salary": "평균 연봉 약 3,500만~6,000만 원"
        }
    ],

    "ISFJ": [
        {
            "career": "간호사 🩺",
            "department": "간호학과",
            "personality": "배려심이 많고 책임감이 강하며 다른 사람을 잘 챙기는 성격",
            "salary": "평균 연봉 약 4,000만~5,000만 원"
        },
        {
            "career": "초등학교 교사 🍎",
            "department": "초등교육과, 교육학과",
            "personality": "인내심이 있고 친절하며 다른 사람을 도와주는 것을 좋아하는 성격",
            "salary": "평균 연봉 약 4,000만~6,000만 원"
        }
    ],

    "INFJ": [
        {
            "career": "상담심리사 💬",
            "department": "심리학과, 상담심리학과",
            "personality": "공감 능력이 좋고 다른 사람의 마음을 깊게 이해하는 성격",
            "salary": "평균 연봉 약 3,000만~4,500만 원"
        },
        {
            "career": "작가 ✍️",
            "department": "문예창작과, 국어국문학과",
            "personality": "상상력이 풍부하고 자신의 생각을 깊이 표현하는 성격",
            "salary": "평균 연봉 약 3,000만~5,000만 원"
        }
    ],

    "INTJ": [
        {
            "career": "데이터 분석가 💻",
            "department": "통계학과, 컴퓨터공학과, 데이터사이언스학과",
            "personality": "논리적이고 분석을 좋아하며 혼자서 집중하는 것을 잘하는 성격",
            "salary": "평균 연봉 약 4,500만~7,000만 원"
        },
        {
            "career": "건축가 🏗️",
            "department": "건축학과, 건축공학과",
            "personality": "계획적이고 논리적이며 새로운 아이디어를 구체화하는 것을 좋아하는 성격",
            "salary": "평균 연봉 약 4,000만~6,000만 원"
        }
    ],

    "ISTP": [
        {
            "career": "제품 디자이너 🎨",
            "department": "산업디자인학과, 제품디자인학과",
            "personality": "실용적이고 문제를 해결하는 것을 좋아하며 손재주가 좋은 성격",
            "salary": "평균 연봉 약 3,500만~5,500만 원"
        },
        {
            "career": "기계공학 기술자 ⚙️",
            "department": "기계공학과, 자동차공학과",
            "personality": "논리적이고 직접 만들어보며 문제를 해결하는 것을 좋아하는 성격",
            "salary": "평균 연봉 약 4,000만~6,000만 원"
        }
    ],

    "ISFP": [
        {
            "career": "파티시에 🧁",
            "department": "제과제빵학과, 호텔제과제빵학과, 식품조리학과",
            "personality": "섬세하고 감각적이며 자신의 창의력을 표현하는 것을 좋아하는 성격",
            "salary": "평균 연봉 약 2,800만~4,000만 원"
        },
        {
            "career": "플로리스트 💐",
            "department": "원예학과, 화훼디자인학과",
            "personality": "감각적이고 섬세하며 아름다운 것을 만드는 것을 좋아하는 성격",
            "salary": "평균 연봉 약 2,800만~4,000만 원"
        }
    ],

    "INFP": [
        {
            "career": "콘텐츠 크리에이터 🎬",
            "department": "미디어학과, 영상학과, 콘텐츠학과",
            "personality": "창의적이고 자신의 생각과 감정을 자유롭게 표현하는 성격",
            "salary": "평균 연봉 약 3,000만~5,000만 원"
        },
        {
            "career": "일러스트레이터 🖌️",
            "department": "시각디자인학과, 일러스트레이션학과",
            "personality": "상상력이 풍부하고 예술적인 표현을 좋아하는 성격",
            "salary": "평균 연봉 약 2,500만~4,500만 원"
        }
    ],

    "INTP": [
        {
            "career": "프로그래머 💻",
            "department": "컴퓨터공학과, 소프트웨어학과",
            "personality": "논리적이고 새로운 원리나 문제를 탐구하는 것을 좋아하는 성격",
            "salary": "평균 연봉 약 4,000만~7,000만 원"
        },
        {
            "career": "연구원 🔬",
            "department": "자연과학과, 생명과학과, 공학계열",
            "personality": "호기심이 많고 한 가지 주제를 깊게 파고드는 성격",
            "salary": "평균 연봉 약 4,000만~6,500만 원"
        }
    ],

    "ESTP": [
        {
            "career": "영업기획자 📈",
            "department": "경영학과, 마케팅학과",
            "personality": "활동적이고 사람들과 소통하는 것을 좋아하며 상황 대처가 빠른 성격",
            "salary": "평균 연봉 약 3,500만~6,000만 원"
        },
        {
            "career": "이벤트 기획자 🎉",
            "department": "광고홍보학과, 이벤트학과, 문화콘텐츠학과",
            "personality": "에너지가 넘치고 즉각적으로 문제를 해결하는 것을 좋아하는 성격",
            "salary": "평균 연봉 약 3,000만~5,000만 원"
        }
    ],

    "ESFP": [
        {
            "career": "방송인 🎤",
            "department": "방송연예과, 미디어학과",
            "personality": "밝고 사교적이며 사람들 앞에서 자신의 매력을 보여주는 것을 좋아하는 성격",
            "salary": "평균 연봉 약 3,000만~6,000만 원"
        },
        {
            "career": "호텔리어 🏨",
            "department": "호텔경영학과, 관광경영학과",
            "personality": "친화력이 좋고 사람을 만나는 것을 좋아하며 서비스 정신이 강한 성격",
            "salary": "평균 연봉 약 3,000만~5,000만 원"
        }
    ],

    "ENFP": [
        {
            "career": "마케팅 기획자 💡",
            "department": "경영학과, 광고홍보학과, 마케팅학과",
            "personality": "아이디어가 많고 사람들과 소통하는 것을 좋아하는 성격",
            "salary": "평균 연봉 약 4,000만~6,500만 원"
        },
        {
            "career": "브랜드 기획자 ✨",
            "department": "경영학과, 디자인학과, 광고홍보학과",
            "personality": "창의적이고 새로운 아이디어를 생각하는 것을 좋아하는 성격",
            "salary": "평균 연봉 약 3,500만~6,000만 원"
        }
    ],

    "ENTP": [
        {
            "career": "창업가 🚀",
            "department": "경영학과, 창업학과, 경제학과",
            "personality": "새로운 아이디어를 내는 것을 좋아하고 도전적인 성격",
            "salary": "수입 차이가 매우 크며 사업 성과에 따라 달라짐"
        },
        {
            "career": "광고기획자 📢",
            "department": "광고홍보학과, 마케팅학과",
            "personality": "아이디어가 많고 새로운 것을 시도하는 것을 좋아하는 성격",
            "salary": "평균 연봉 약 3,500만~6,000만 원"
        }
    ],

    "ESTJ": [
        {
            "career": "경영 관리자 📋",
            "department": "경영학과, 경제학과",
            "personality": "책임감이 강하고 일을 체계적으로 관리하는 성격",
            "salary": "평균 연봉 약 4,500만~7,000만 원"
        },
        {
            "career": "회계·세무 전문가 💰",
            "department": "회계학과, 세무학과",
            "personality": "꼼꼼하고 현실적이며 숫자와 규칙을 잘 다루는 성격",
            "salary": "평균 연봉 약 4,000만~6,500만 원"
        }
    ],

    "ESFJ": [
        {
            "career": "호텔리어 🏨",
            "department": "호텔경영학과, 관광경영학과",
            "personality": "친화력이 좋고 다른 사람을 챙기는 것을 좋아하는 성격",
            "salary": "평균 연봉 약 3,000만~5,000만 원"
        },
        {
            "career": "교사 🍎",
            "department": "교육학과, 사범대학 관련 학과",
            "personality": "책임감이 강하고 사람들과 협력하는 것을 좋아하는 성격",
            "salary": "평균 연봉 약 4,000만~6,000만 원"
        }
    ],

    "ENFJ": [
        {
            "career": "교사 👩‍🏫",
            "department": "교육학과, 사범대학 관련 학과",
            "personality": "사람을 이끌고 도와주는 것을 좋아하며 공감 능력이 좋은 성격",
            "salary": "평균 연봉 약 4,000만~6,000만 원"
        },
        {
            "career": "홍보 전문가 📣",
            "department": "광고홍보학과, 미디어학과",
            "personality": "소통 능력이 좋고 사람들과 관계를 만드는 것을 좋아하는 성격",
            "salary": "평균 연봉 약 3,500만~6,000만 원"
        }
    ],

    "ENTJ": [
        {
            "career": "기업 경영자 💼",
            "department": "경영학과, 경제학과",
            "personality": "목표가 뚜렷하고 사람들을 이끌며 계획을 세우는 것을 좋아하는 성격",
            "salary": "직업과 기업 규모에 따라 큰 차이가 있음"
        },
        {
            "career": "프로젝트 매니저 📊",
            "department": "경영학과, 산업공학과",
            "personality": "리더십이 있고 계획적으로 일을 진행하는 성격",
            "salary": "평균 연봉 약 5,000만~8,000만 원"
        }
    ]
}


# -----------------------------
# 화면
# -----------------------------

st.title("🧭 MBTI 진로 추천 테스트")
st.subheader("✨ 나에게 어울리는 진로는 무엇일까?")

st.write(
    "MBTI 유형을 하나 골라보세요! "
    "나와 잘 맞는 진로 2가지를 추천해드릴게요 😊"
)

st.info("💡 진로 추천은 참고용이에요. MBTI가 진로를 결정하는 것은 아니랍니다!")


# MBTI 선택
mbti_list = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

selected_mbti = st.selectbox(
    "👇 나의 MBTI를 선택해주세요!",
    mbti_list
)


# 추천 버튼
if st.button("🚀 나에게 맞는 진로 찾아보기", use_container_width=True):

    st.success(f"🎉 {selected_mbti}에게 추천하는 진로를 알려드릴게요!")

    careers = career_data[selected_mbti]

    for i, career in enumerate(careers, 1):

        st.markdown("---")

        st.header(f"{i}️⃣ {career['career']}")

        st.write(f"🎓 **추천 학과**")
        st.write(career["department"])

        st.write(f"🧠 **잘 맞는 성격**")
        st.write(career["personality"])

        st.write(f"💰 **평균 연봉**")
        st.write(career["salary"])

    st.markdown("---")

    st.success(
        "🌱 진로를 고를 때는 MBTI뿐만 아니라 "
        "내가 좋아하는 것, 잘하는 것, 관심 있는 분야도 함께 생각해보세요!"
    )

st.caption("💫 나의 적성과 관심사를 찾아가는 것도 멋진 진로 탐색이에요!")
