# Save this file as app.py
import streamlit as st
import pandas as pd
import datetime as dt
from io import BytesIO

# 🎯 App Config
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

    # 📅 Calculate "today" based on max date
    today_date = df['date'].max() + pd.Timedelta(days=1)


    # 🧠 RFM Calculation
    rfm = df.groupby(['branch', 'route', 'CustomerName']).agg({
        'date': lambda x: (today_date - x.max()).days,
        'InvoiceNumber': 'nunique',
        'NetAmount': 'sum'
    })
    rfm.columns = ['Recency', 'Frequency', 'Monetary']

    # 🧮 RFM Scoring
    rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1]).astype(int)
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
    rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5]).astype(int)

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

    # 📥 Download Button
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=True, sheet_name='RFM_Analysis')
        processed_data = output.getvalue()
        return processed_data

    excel_data = to_excel(rfm)

    st.download_button(
        label="📥 Download RFM Segmented Data as Excel",
        data=excel_data,
        file_name='rfm_analysis.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

else:
    st.warning('⚠️ Please upload a Sales Excel file to proceed.')

# 📝 Footer
st.markdown("""
---
Made with ❤️ using **Streamlit** | Powered for FMCG sales analytics 🚚
""")
