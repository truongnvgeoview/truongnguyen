import streamlit as st
import pandas as pd
from datetime import datetime
from db import fetch_inventory, add_inventory, delete_inventory, fetch_sales, sell_device

st.set_page_config(page_title="📱 QUỐC HÙNG Mobile - PHẦN MỀM QUẢN LÝ", layout="wide")
st.title(" QUỐC HÙNG Mobile - Phần Mềm Quản Lý Kho")

# ===== LOAD DỮ LIỆU =====
inventory = fetch_inventory()
sales = fetch_sales()

col1, col2 = st.columns([1, 2])

# ===== NHẬP MÁY MỚI =====
with col1:
    with st.form("form_nhap"):
        st.subheader("➕ Nhập máy mới")

        model_base_option = st.selectbox("📱 Dòng máy", [
            "iPhone 12", "iPhone 13", "iPhone 14", "iPhone 15", "iPhone 16", "Samsung", "Khác"
        ])
        if model_base_option == "Khác":
            model_base = st.text_input("Nhập dòng máy khác").strip()
        else:
            model_base = model_base_option

        model_type = st.selectbox("📌 Kiểu máy", ["Thường", "Pro", "Pro Max"])
        storage_choice = st.selectbox("💾 Dung lượng", ["128GB", "256GB", "512GB", "Khác"])
        model_storage = st.text_input("Nhập dung lượng khác") if storage_choice == "Khác" else storage_choice

        imei = st.text_input("🔢 IMEI", max_chars=30).strip()
        gia_nhap = st.number_input("💰 Giá Nhập (nghìn KRW)", min_value=1)
        tinh_trang = st.text_input("⚙️ Tình Trạng", max_chars=100).strip()

        submit = st.form_submit_button("✅ Thêm vào kho")

        if submit:
            full_model = f"{model_base} {model_type} {model_storage}"
            full_price = gia_nhap * 1000

            if not model_base or not model_storage or not imei or not tinh_trang:
                st.error("❌ Vui lòng nhập đầy đủ.")
            elif len(imei) < 5:
                st.error("❌ IMEI phải dài ít nhất 5 ký tự.")
            elif imei in inventory['imei'].astype(str).values:
                st.warning("⚠️ IMEI này đã tồn tại trong kho.")
            else:
                add_inventory(full_model, imei, full_price, tinh_trang)
                st.success("✔️ Máy đã được thêm vào kho.")
                st.rerun()

# ===== DANH SÁCH MÁY HIỆN CÓ =====
with col2:
    st.subheader("📦 Danh sách máy hiện có")

    search = st.text_input("🔍 Tìm kiếm theo Model hoặc IMEI").lower().strip()
    filtered = inventory[
        inventory['model'].str.lower().str.contains(search) |
        inventory['imei'].astype(str).str.lower().str.contains(search)
    ] if search else inventory

    if not filtered.empty:
        header = st.columns([3, 2, 2, 3, 1, 1])
        header[0].markdown("**📱 Model**")
        header[1].markdown("**🔢 IMEI**")
        header[2].markdown("**💰 Giá Nhập**")
        header[3].markdown("**⚙️ Tình Trạng**")
        header[4].markdown("**📤 Bán**")
        header[5].markdown("**🗑️ Xoá**")

    for i, row in filtered.iterrows():
        cols = st.columns([3, 2, 2, 3, 1, 1])
        cols[0].markdown(row['model'])
        cols[1].markdown(f"`{row['imei']}`")
        cols[2].markdown(f"{int(row['gia_nhap']):,}₩")
        cols[3].markdown(row['tinh_trang'])

        if cols[4].button("📤", key=f"ban_{i}"):
            sell_device(row['imei'])
            st.success(f"✅ Đã bán máy: {row['model']} ({row['imei']})")
            st.rerun()

        if cols[5].button("🗑️", key=f"xoa_{i}"):
            delete_inventory(row['imei'])
            st.warning(f"🗑️ Đã xoá máy: {row['model']} ({row['imei']})")
            st.rerun()

# ===== MÁY ĐÃ BÁN =====
with st.expander("📋 Xem danh sách máy đã bán"):
    if sales.empty:
        st.info("Chưa có máy nào được bán.")
    else:
        sales['gia_nhap'] = sales['gia_nhap'].apply(lambda x: f"{int(x):,}₩")
        st.dataframe(sales, use_container_width=True)
