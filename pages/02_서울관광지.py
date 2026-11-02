import streamlit as st
import folium
from streamlit_folium import st_folium


# ==========================================
# 페이지 설정
# ==========================================

st.set_page_config(
    page_title="서울 관광지 TOP 10",
    page_icon="🗺️",
    layout="wide"
)


# ==========================================
# 제목
# ==========================================

st.title("🗺️ 서울 외국인 인기 관광지 TOP 10")

st.write(
    "서울을 방문하는 외국인 관광객들이 많이 찾는 "
    "서울의 대표 관광지를 지도에서 확인해보세요!"
)


# ==========================================
# 서울 관광지 TOP 10
# ==========================================

places = [
    {
        "rank": 1,
        "name": "경복궁",
        "lat": 37.5796,
        "lon": 126.9770,
        "description": "조선의 대표 궁궐로 한국의 전통 건축과 역사를 경험할 수 있는 서울의 대표 관광지입니다."
    },

    {
        "rank": 2,
        "name": "N서울타워",
        "lat": 37.5512,
        "lon": 126.9882,
        "description": "남산에 위치한 서울의 대표 랜드마크로 서울의 아름다운 전경을 한눈에 볼 수 있습니다."
    },

    {
        "rank": 3,
        "name": "명동",
        "lat": 37.5636,
        "lon": 126.9826,
        "description": "쇼핑과 K-뷰티, 길거리 음식 등을 즐길 수 있어 외국인 관광객에게 인기 있는 지역입니다."
    },

    {
        "rank": 4,
        "name": "북촌한옥마을",
        "lat": 37.5826,
        "lon": 126.9830,
        "description": "전통 한옥이 모여 있는 곳으로 한국의 옛 모습과 전통적인 분위기를 경험할 수 있습니다."
    },

    {
        "rank": 5,
        "name": "홍대",
        "lat": 37.5563,
        "lon": 126.9236,
        "description": "거리공연과 패션, 카페, 다양한 문화 콘텐츠를 즐길 수 있는 활기찬 관광지입니다."
    },

    {
        "rank": 6,
        "name": "광장시장",
        "lat": 37.5700,
        "lon": 126.9997,
        "description": "빈대떡과 김밥 등 다양한 한국 음식을 맛보고 전통시장 분위기를 경험할 수 있습니다."
    },

    {
        "rank": 7,
        "name": "동대문디자인플라자(DDP)",
        "lat": 37.5669,
        "lon": 127.0095,
        "description": "독특한 건축 디자인과 전시, 패션 및 문화 행사를 즐길 수 있는 서울의 랜드마크입니다."
    },

    {
        "rank": 8,
        "name": "인사동",
        "lat": 37.5740,
        "lon": 126.9857,
        "description": "전통 공예품과 갤러리, 기념품 가게 등이 모여 있어 한국 전통문화를 체험하기 좋은 곳입니다."
    },

    {
        "rank": 9,
        "name": "청계천",
        "lat": 37.5690,
        "lon": 126.9787,
        "description": "서울 도심을 흐르는 하천으로 산책하면서 서울의 도시 풍경을 여유롭게 즐길 수 있습니다."
    },

    {
        "rank": 10,
        "name": "롯데월드타워·서울스카이",
        "lat": 37.5126,
        "lon": 127.1025,
        "description": "서울의 현대적인 모습을 보여주는 랜드마크로 전망대에서 서울의 멋진 풍경을 볼 수 있습니다."
    }
]


# ==========================================
# 서울 지도 생성
# ==========================================

seoul_map = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12,
    tiles="OpenStreetMap"
)


# ==========================================
# 관광지 마커 추가
# ==========================================

for place in places:

    popup_html = f"""
    <div style="width: 250px;">
        <h3>
            {place["rank"]}. {place["name"]}
        </h3>

        <p>
            {place["description"]}
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


# ==========================================
# 지도 표시
# ==========================================

st.subheader("📍 서울 관광지 지도")

st_folium(
    seoul_map,
    width=None,
    height=600
)


# ==========================================
# 관광지 설명
# ==========================================

st.subheader("📖 관광지 간단 소개")


for place in places:

    st.markdown(
        f"### {place['rank']}. {place['name']}"
    )

    st.write(
        place["description"]
    )

    st.divider()
