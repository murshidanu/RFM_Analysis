import pandas as pd


def load_data(uploaded_file):
    """Shared function to load either Excel or CSV"""
    try:
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)

        # Convert date column if exists
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])

        return df

    except Exception as e:
        raise ValueError(f"Error loading file: {str(e)}")