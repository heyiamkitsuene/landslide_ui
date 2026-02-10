import streamlit as st
from PIL import Image
import random
import folium
from streamlit_folium import st_folium

# -------------------------------
st.set_page_config(page_title="山泥傾瀉風險評估", layout="wide")
st.title("🏔️ 強化版山泥傾瀉風險 App")

# -------------------------------
# Sidebar
st.sidebar.header("⚙️ 設置 / 設定")
unit = st.sidebar.selectbox("單位", ["公尺", "英尺"])
language = st.sidebar.selectbox("語言", ["中文", "英文"])
notify_pref = st.sidebar.multiselect("通知偏好", ["AI 判斷結果", "緊急警報"])
st.sidebar.markdown("---")
st.sidebar.subheader("📰 最新新聞")
st.sidebar.markdown("- [CEDD 最新滑坡公告](https://www.cedd.gov.hk/)")
st.sidebar.markdown("- [香港天文台颱風訊息](https://www.hko.gov.hk/)")

# -------------------------------
# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "風險地圖", "安全知識", "天氣 & 聯絡"])

# -------------------------------
# Tab 1: Dashboard
with tab1:
    st.subheader("📸 上傳坡面照片")
    uploaded_file = st.file_uploader("選擇照片 (jpg/png)", type=["jpg","png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="✅ 已上傳照片", use_column_width=True)
        ai_result = random.choice(["無風險", "準備發生", "正在發生"])
        st.write(f"📸 AI 模擬判斷：{ai_result}")
    else:
        st.info("請上傳坡面照片")

    st.subheader("📊 輸入坡面資訊")
    slope = st.slider("📐 坡度角（度）", 0, 60, 30)
    soil = st.selectbox("🌱 土壤類型", ["黏土", "砂土", "岩石"])
    water = st.slider("💧 含水量 (%)", 0, 100, 30)
    veg = st.slider("🌳 植被覆蓋率 (%)", 0, 100, 50)

    # 計算 Fs
    def calculate_fs(slope, water):
        fs = (1 / (1 + water/100)) * (1 / (1 + slope/60))
        return round(fs, 2)

    def calculate_risk_score(slope, soil, water, veg):
        score = 0
        score += 30 if slope > 40 else 20 if slope > 30 else 10
        score += 25 if soil == "黏土" else 15 if soil == "砂土" else 5
        score += 25 if water > 40 else 15 if water > 25 else 5
        score += 20 if veg < 30 else 10 if veg < 60 else 5
        return score

    def determine_level(score):
        if score >= 75:
            return "極高風險"
        elif score >= 55:
            return "高風險"
        elif score >= 35:
            return "中風險"
        else:
            return "低風險"

    fs = calculate_fs(slope, water)
    score = calculate_risk_score(slope, soil, water, veg)
    level =
