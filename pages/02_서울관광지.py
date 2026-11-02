import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(
    page_title="서울 외국인 인기 관광지 TOP 10",
    page_icon="🗺️",
    layout="wide"
)

# 제목
st.title("🗺️ 서울 외국인 인기 관광지 TOP 10")
st.caption(
    "서울의 대표 관광지를 중심으로 외국인 관광객에게 인기 있는 "
    "서울 관광지 10곳을 소개합니다."
)

# 관광지 정보
places = [
    {
        "rank": 1,
        "name": "경복궁",
        "lat": 37.5796,
        "lon": 126.9770,
        "desc": "조선의 대표 궁궐로 한국의 전통 건축과 역사를 느낄 수 있는 서울의 대표 관광지입니다."
    },
    {
        "rank": 2,
        "name": "N서울타워",
        "lat": 37.5512,
        "lon": 126.9882,
        "desc": "남산 정상에서 서울의 전경을 한눈에 볼 수 있는 서울의 대표 랜드마크입니다."
    },
    {
        "rank": 3,
        "name": "명동",
        "lat": 37.5636,
        "lon": 126.9826,
        "desc": "쇼핑, K-뷰티, 길거리 음식 등을 한곳에서 즐길 수 있어 외국인 관광객에게 인기 있는 지역입니다."
    },
    {
        "rank": 4,
        "name": "북촌한옥마을",
        "lat": 37.5826,
        "lon": 126.9830,
        "desc": "전통 한옥이 이어지는 골목을 걸으며 서울의 옛 모습과 한국적인 분위기를 경험할 수 있습니다."
    },
    {
        "rank": 5,
        "name": "홍대",
        "lat": 37.5563,
        "lon": 126.9236,
        "desc": "거리공연, 패션, 카페와 다양한 문화 콘텐츠를 즐길 수 있는 젊고 활기찬 관광지입니다."
    },
    {
        "rank": 6,
        "name": "광장시장",
        "lat": 37.5700,
        "lon": 126.9997,
        "desc": "빈대떡, 김밥 등 한국의 다양한 먹거리를 맛보고 전통시장 분위기를 경험할 수 있습니다."
    },
    {
        "rank": 7,
        "name": "동대문디자인플라자(DDP)",
        "lat": 37.5669,
        "lon": 127.0095,
        "desc": "독특한 건축 디자인과 전시, 패션과 문화 행사를 즐길 수 있는 서울의 현대적인 랜드마크입니다."
    },
    {
        "rank": 8,
        "name": "인사동",
        "lat": 37.5740,
        "lon": 126.9857,
        "desc": "전통 공예품과 갤러리, 기념품 가게 등이 모여 있어 한국의 전통문화를 체험하기 좋은 곳입니다."
    },
    {
        "rank": 9,
        "name": "청계천",
        "lat": 37.5690,
        "lon": 126.9787,
        "desc": "도심 한가운데를 흐르는 하천을 따라 산책하며 서울의 도시 풍경을 여유롭게 즐길 수 있습니다."
    },
    {
        "rank": 10,
        "name": "롯데월드타워·서울스카이",
        "lat": 37.5126,
        "lon": 127.1025,
        "desc": "서울의 현대적인 모습을 볼 수 있는 초고층 랜드마크로 전망대에서 멋진 도시 풍경을 감상할 수 있습니다."
    }
]

# -------------------------
# 서울 지도 만들기
# -------------------------

seoul_map = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12,
    tiles="OpenStreetMap"
)

# 관광지 마커 추가
for place in places:

    popup_html = f"""
    <div style="width:230px;">
        <h4>
            {place['rank']}. {place['name']}
        </h4>

        <p>
            {place['desc']}
        </p>
    </div>
    """

    folium.Marker(
        location=[
            place["lat"],
            place["lon"]
        ],

        popup=folium.Popup(
            popup_html,
            max_width=300
        ),

        tooltip=f"{place['rank']}. {place['name']}",

        icon=folium.Icon(
            color="red",
            icon="star"
        )
    ).add_to(seoul_map)


# -------------------------
# 지도 화면
# -------------------------

st.subheader("📍 서울 관광지 지도")

st_folium(
    seoul_map,
    width=None,
    height=600
)


# -------------------------
# 관광지 설명
# -------------------------

st.subheader("📖 관광지 간단 소개")

for place in places:

    st.markdown(
        f"### {place['rank']}. {place['name']}"
    )

    st.write(
        place["desc"]
    )

    st.divider()
