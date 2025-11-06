# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 09:55:30 2025
@author: huyentt
"""

# -*- coding: utf-8 -*-
import streamlit as st
import os
import re
import warnings

warnings.filterwarnings("ignore")

# --- Cấu hình trang ---
st.set_page_config(page_title="📖 Web đọc truyện của Huyền", layout="wide")

# --- CSS giao diện nền tối và style ---
st.markdown("""
<style>
.stApp, body, .main { background-color: #0E1117 !important; color: white !important; }
.title { font-size: 28px; font-weight: bold; color: #ffb6c1; }
.author { font-size: 16px; color: #80cbc4; margin-bottom: 10px; }
.tag { display: inline-block; background-color: #1f1f1f; color: #f1f1f1; border-radius: 15px; padding: 5px 12px; margin: 4px; font-size: 13px; }
.stSelectbox label, .stSelectbox div, .stMarkdown, .stSubheader, .stTextInput label { color: white !important; }
hr { border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# --- Đọc dữ liệu truyện từ folder local ---
DATA_PATH = "data"  # folder chứa thư mục truyện
truyen = {}

for folder_name in os.listdir(DATA_PATH):
    folder_path = os.path.join(DATA_PATH, folder_name)
    if os.path.isdir(folder_path):
        match = re.match(r"(.+)_\[(.+)\]_\[(.+)\]", folder_name)
        if not match:
            continue
        ten_truyen, tac_gia, the_loai_str = match.groups()
        the_loai = the_loai_str.split("_")

        files = os.listdir(folder_path)
        chuong_dict = {}
        anh = None

        for f in files:
            if f.lower().endswith(('.jpg', '.png', '.jpeg')):
                anh = os.path.join(folder_path, f)
            elif f.startswith("Chương"):
                with open(os.path.join(folder_path, f), "r", encoding="utf-8") as file:
                    chuong_dict[f] = file.read()

        truyen[ten_truyen] = {
            "tac_gia": tac_gia,
            "anh": anh,
            "the_loai": the_loai,
            "chuong": chuong_dict
        }

# --- Giao diện Streamlit ---
if truyen:
    chon_truyen = st.selectbox("📚 Chọn truyện", list(truyen.keys()))
    info = truyen[chon_truyen]

    col1, col2 = st.columns([1, 2])

    with col1:
        if info["anh"]:
            st.image(info["anh"], use_container_width=True)
        else:
            st.markdown("*Không có ảnh bìa*")

    with col2:
        st.markdown(f"<div class='title'>{chon_truyen}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='author'>Tác giả: {info['tac_gia']}</div>", unsafe_allow_html=True)
        st.markdown("".join([f"<span class='tag'>{tl}</span>" for tl in info["the_loai"]]), unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    chon_chuong = st.selectbox("📘 Chọn chương", list(info["chuong"].keys()))
    st.subheader(chon_chuong)
    st.markdown(
        f"<div style='font-size:17px; line-height:1.7; white-space:pre-wrap;'>{info['chuong'][chon_chuong]}</div>",
        unsafe_allow_html=True
    )
else:
    st.warning("⚠️ Không tìm thấy truyện nào trong thư mục data!")

