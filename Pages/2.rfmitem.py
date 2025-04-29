import streamlit as st
import pandas as pd
import datetime as dt
from io import BytesIO

# � App Config
st.set_page_config(page_title="FMCG RFM Analysis App", page_icon="📈", layout="wide")

# 🎨 Sidebar
st.sidebar.header("Settings")
st.sidebar.write("Upload your FMCG sales data to perform RFM Analysis.")

# 🏷️ Main Title
st.title('📊 FMCG Customer RFM Analysis')

# 📂 Upload file
uploaded_file = st.file_uploader("Upload Sales Excel File", type=["xlsx"])

if uploaded_file:
    # 🧹 Read Data
    df = pd.read_excel(uploaded_file)
    df['date'] = pd.to_datetime(df['date'])

    st.success('✅ File uploaded successfully!')

    # 👀 Preview Data
    with st.expander("🔎 Preview Uploaded Data"):
        st.dataframe(df.head())
    df['InvoiceNumber'] = df['InvoiceNumber'].astype(str)

    # Dropdowns for category & product
    category_column = 'SubCategoryName'
    product_column = 'StockName'

    # Get unique categories
    categories = ["All"] + sorted(df[category_column].dropna().unique().tolist())
    selected_category = st.sidebar.selectbox("Select Category", categories)

    # Filter products based on selected category
    if selected_category != "All":
        filtered_products = df[df[category_column] == selected_category][product_column].unique()
    else:
        filtered_products = df[product_column].unique()

    products = ["All"] + sorted(filtered_products.tolist())
    selected_product = st.sidebar.selectbox("Select Product", products)

    # 🟩 Apply button
    if st.sidebar.button("🚀 Apply"):
        filtered_df = df.copy()

        # Apply category filter
        if selected_category != "All":
            filtered_df = filtered_df[filtered_df[category_column] == selected_category]

        # Apply product filter
        if selected_product != "All":
            filtered_df = filtered_df[filtered_df[product_column] == selected_product]

        if filtered_df.empty:
            st.warning("⚠️ No data available for the selected filters.")
        else:
            today_date = filtered_df['date'].max()  # Use last date in data

            # � RFM Calculation
            rfm = filtered_df.groupby(['branch', 'route', 'CustomerName']).agg({
                'date': lambda x: (today_date - x.max()).days,
                'InvoiceNumber': 'nunique',
                'NetAmount': 'sum'
            })
            rfm.columns = ['Recency', 'Frequency', 'Monetary']

            # 🧮 RFM Scoring
            rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
            rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
            rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5]).astype(int)

            rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)


            # ✨ Segmentation
            def segment(row):
                if row['R_Score'] == 5 and row['F_Score'] == 5:
                    return 'Champions'
                elif row['R_Score'] >= 4 and row['F_Score'] >= 4:
                    return 'Loyal Customers'
                elif row['R_Score'] == 5 and row['F_Score'] <= 3:
                    return 'New Customers'
                elif row['R_Score'] <= 2 and row['F_Score'] >= 4:
                    return "Can't Lose Them"
                elif row['R_Score'] <= 2 and row['F_Score'] <= 3:
                    return "At Risk"
                elif row['R_Score'] == 1 and row['F_Score'] <= 2:
                    return "Lost Customers"
                elif row['F_Score'] >= 4:
                    return "Frequent Buyers"
                elif row['M_Score'] >= 4:
                    return "Big Spenders"
                else:
                    return "Others"


            rfm['Segment'] = rfm.apply(segment, axis=1)

            # 📊 Display RFM Table
            st.subheader("🧩 RFM Segmentation Results")
            st.dataframe(rfm.reset_index())

            # 📥 Download Button with filter info
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                rfm.reset_index().to_excel(writer, sheet_name='RFM_Analysis', index=False)

            st.download_button(
                label="📥 Download RFM Results",
                data=output.getvalue(),
                file_name=f"RFM_Analysis_{selected_category}_{selected_product}.xlsx",
                mime="application/vnd.ms-excel"
            )