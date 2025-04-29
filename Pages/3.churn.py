import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
from io import BytesIO

# Set page config
st.set_page_config(page_title="FMCG Churn Analysis", page_icon="📊", layout="wide")

# Title
st.title("📈 FMCG Product Churn Analysis")

# Sidebar for file upload
with st.sidebar:
    st.header("Upload Data")
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

    st.header("Settings")
    CHURN_THRESHOLD = st.slider("Churn Threshold (months)", 1, 12, 3)
    st.caption("Customers who haven't purchased in this many months are considered churned")

if uploaded_file:
    # Load data
    df = pd.read_excel(uploaded_file)

    # Convert date column
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    else:
        st.error("The dataset must contain a 'date' column")
        st.stop()

    # Item selection
    st.subheader("Select Product for Analysis")
    item_name = st.selectbox(
        "Choose a product:",
        sorted(df['StockName'].unique()),
        index=0
    )

    # Filter data
    filtered_df = df[df['StockName'] == item_name].copy()

    if filtered_df.empty:
        st.warning(f"No data found for product: {item_name}")
    else:
        # --- Cohort Analysis ---
        st.subheader("Cohort Retention Analysis")

        filtered_df['CohortMonth'] = filtered_df.groupby('CustomerName')['date'].transform('min').dt.to_period('M')
        filtered_df['OrderMonth'] = filtered_df['date'].dt.to_period('M')
        filtered_df['MonthsSinceFirstPurchase'] = (filtered_df['OrderMonth'] - filtered_df['CohortMonth']).apply(
            lambda x: x.n)

        cohort_data = filtered_df.groupby(['CohortMonth', 'MonthsSinceFirstPurchase'])[
            'CustomerName'].nunique().reset_index()
        cohort_pivot = cohort_data.pivot_table(index='CohortMonth', columns='MonthsSinceFirstPurchase',
                                               values='CustomerName', aggfunc='sum')
        retention_matrix = (cohort_pivot.divide(cohort_pivot.iloc[:, 0], axis=0) * 100).round(1)

        # Display retention matrix
        st.write("**Retention Matrix (% of customers retained)**")
        st.dataframe(retention_matrix.style.background_gradient(cmap='Blues'))

        # Heatmap visualization
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.heatmap(retention_matrix, annot=True, fmt='.1f', cmap='Blues', cbar=False, ax=ax1)
        ax1.set_title(f'Retention for {item_name} (%)')
        st.pyplot(fig1)

        # --- Churn Analysis ---
        st.subheader("Churn Analysis")

        last_purchase = filtered_df.groupby('CustomerName')['date'].max().reset_index()
        latest_date = filtered_df['date'].max()
        last_purchase['MonthsSinceLastPurchase'] = (latest_date - last_purchase['date']).dt.days // 30
        last_purchase['Churned'] = last_purchase['MonthsSinceLastPurchase'] > CHURN_THRESHOLD
        churned_customers = last_purchase[last_purchase['Churned']].merge(filtered_df, on='CustomerName', how='left')

        # Calculate churn rate
        monthly_churn = last_purchase.groupby(last_purchase['date'].dt.to_period('M'))['Churned'].mean() * 100

        # Display churn metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Customers", len(last_purchase))
            st.metric("Churned Customers",
                      f"{len(churned_customers)} ({len(churned_customers) / len(last_purchase) * 100:.1f}%)")

        with col2:
            st.write("**Monthly Churn Rate Trend**")
            fig2, ax2 = plt.subplots(figsize=(10, 4))
            monthly_churn.plot(kind='line', marker='o', ax=ax2)
            ax2.set_title(f'Monthly Churn Rate for {item_name} (%)')
            ax2.set_ylabel('Churn Rate')
            st.pyplot(fig2)

        # Show churned customers table
        with st.expander("View Churned Customers Details"):
            st.dataframe(churned_customers)

        # --- Download Report ---
        st.subheader("Download Report")

        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Sheet 1: Retention Matrix
            retention_matrix.to_excel(writer, sheet_name='Retention Matrix')

            # Sheet 2: Churned Customers
            churned_customers.to_excel(writer, sheet_name='Churned Customers', index=False)

            # Add plots to Excel
            workbook = writer.book
            worksheet = workbook.add_worksheet('Plots')

            # Save plots to BytesIO objects
            fig1_bytes = BytesIO()
            fig1.savefig(fig1_bytes, format='png', bbox_inches='tight')

            fig2_bytes = BytesIO()
            fig2.savefig(fig2_bytes, format='png', bbox_inches='tight')

            # Insert images
            worksheet.insert_image('B2', '', {'image_data': fig1_bytes})
            worksheet.insert_image('B30', '', {'image_data': fig2_bytes})

        # Download button
        st.download_button(
            label="📥 Download Full Report (Excel)",
            data=output.getvalue(),
            file_name=f"Churn_Analysis_{item_name.replace(' ', '_')}.xlsx",
            mime="application/vnd.ms-excel"
        )
else:
    st.info("👈 Please upload an Excel file to begin analysis")