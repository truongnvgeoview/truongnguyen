import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==== ĐƯỜNG DẪN FILE ====
INVENTORY_FILE = 'data/inventory.csv'
BANHANG_FILE = 'data/banhang.csv'

# ==== TẠO THƯ MỤC ====
os.makedirs("data", exist_ok=True)

# ==== LOAD DỮ LIỆU ====
def load_inventory():
    if os.path.exists(INVENTORY_FILE):
        return pd.read_csv(INVENTORY_FILE)
    return pd.DataFrame(columns=['Model', 'IMEI', 'Giá Nhập', 'Tình Trạng'])

def load_sales():
    if os.path.exists(BANHANG_FILE):
        try:
            return pd.read_csv(BANHANG_FILE)
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=['Model', 'IMEI', 'Giá Nhập', 'Tình Trạng', 'Ngày Bán'])
    else:
        return pd.DataFrame(columns=['Model', 'IMEI', 'Giá Nhập', 'Tình Trạng', 'Ngày Bán'])

def save_inventory(df):
    df.to_csv(INVENTORY_FILE, index=False)

def save_sales(df):
    df.to_csv(BANHANG_FILE, index=False)

# ==== GIAO DIỆN ====
st.set_page_config(page_title="📱 QUỐC HÙNG Mobile - PHẦN MỀM QUẢN LÝ", layout="wide")
st.title(" QUỐC HÙNG  Mobile - Phần Mềm Quản Lý Kho")

inventory = load_inventory()
sales = load_sales()

col1, col2 = st.columns([1, 2])

# ==== NHẬP MÁY ====
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

        if storage_choice == "Khác":
            storage_custom = st.text_input("Nhập dung lượng khác (ví dụ: 1TB)").strip()
            model_storage = storage_custom
        else:
            model_storage = storage_choice

        imei = st.text_input("🔢 IMEI", max_chars=30).strip()
        gia_nhap = st.number_input("💰 Giá Nhập (nghìn KRW)", min_value=1)
        tinh_trang = st.text_input("⚙️ Tình Trạng (pin, màn, Face ID...)", max_chars=100).strip()

        submit = st.form_submit_button("✅ Thêm vào kho")

        if submit:
            full_model = f"{model_base} {model_type} {model_storage}"
            full_price = gia_nhap * 1000

            if not model_base or not model_storage or not imei or not tinh_trang:
                st.error("❌ Vui lòng nhập đầy đủ tất cả các trường.")
            elif len(imei) < 5:
                st.error("❌ IMEI phải dài ít nhất 5 ký tự.")
            elif imei in inventory['IMEI'].astype(str).values:
                st.warning("⚠️ IMEI này đã tồn tại trong kho!")
            else:
                new_row = pd.DataFrame([[full_model, imei, full_price, tinh_trang]], columns=inventory.columns)
                inventory = pd.concat([inventory, new_row], ignore_index=True)
                save_inventory(inventory)
                st.success("✔️ Máy mới đã được thêm vào kho!")

# ==== DANH SÁCH MÁY HIỆN CÓ ====
with col2:
    st.subheader("📦 Danh sách máy hiện có")

    search = st.text_input("🔍 Tìm kiếm theo Model hoặc IMEI").lower().strip()
    if search:
        filtered = inventory[
            inventory['Model'].str.lower().str.contains(search) |
            inventory['IMEI'].astype(str).str.lower().str.contains(search)
        ]
    else:
        filtered = inventory

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
        cols[0].markdown(f"{row['Model']}")
        cols[1].markdown(f"`{row['IMEI']}`")
        cols[2].markdown(f"{int(row['Giá Nhập']):,}₩")
        cols[3].markdown(f"{row['Tình Trạng']}")

        # 📤 BÁN
        if cols[4].button("📤", key=f"ban_{i}"):
            ngay_ban = datetime.now().strftime("%Y-%m-%d")
            sold_row = pd.DataFrame([[row['Model'], row['IMEI'], row['Giá Nhập'], row['Tình Trạng'], ngay_ban]],
                                    columns=['Model', 'IMEI', 'Giá Nhập', 'Tình Trạng', 'Ngày Bán'])
            sales = pd.concat([sales, sold_row], ignore_index=True)
            save_sales(sales)

            inventory.drop(index=i, inplace=True)
            inventory.reset_index(drop=True, inplace=True)
            save_inventory(inventory)
            st.success(f"✅ Đã bán máy: {row['Model']} ({row['IMEI']})")
            st.experimental_rerun()

        # 🗑️ XOÁ
        if cols[5].button("🗑️", key=f"xoa_{i}"):
            inventory.drop(index=i, inplace=True)
            inventory.reset_index(drop=True, inplace=True)
            save_inventory(inventory)
            st.warning(f"🗑️ Đã xoá máy: {row['Model']} ({row['IMEI']})")
            st.experimental_rerun()

# ==== MÁY ĐÃ BÁN ====
with st.expander("📋 Xem danh sách máy đã bán"):
    if sales.empty:
        st.info("Chưa có máy nào được bán.")
    else:
        display_sales = sales.copy()
        display_sales['Giá Nhập'] = display_sales['Giá Nhập'].apply(lambda x: f"{int(x):,}₩")
        st.dataframe(display_sales, use_container_width=True)
