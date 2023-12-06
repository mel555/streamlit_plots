import streamlit as st
import pandas as pd
import plotly.express as px
import os

def load_and_filter_data():
    file_path = os.path.dirname(os.path.abspath(__file__))
    data = 'ames.csv'
    data_path = os.path.join(file_path,data)

    df = pd.read_csv(data_path)
    df_selected_cols = df[["Order", "Lot Area", "Yr Sold", "Mo Sold", "Year Built", "SalePrice"]]
    df_selected_cols["house_age"] = df_selected_cols["Yr Sold"] - df_selected_cols["Year Built"]

    return df_selected_cols

# Create dropdown list widget
def headers_dropdown_list(df):
    dataframe_headers = list(df)
    headers = st.sidebar.selectbox('Select header:', dataframe_headers)

    return headers

# create slider for filtering house age
def create_slider(df, column, label):
    min_val = min(df[column])
    max_val = max(df[column])
    slider = st.slider(label=label, min_value=min_val, max_value=max_val, value=(min_val, max_val))

    return slider

# Create plot that is filtered using the dropdown
def sale_price_scatter(df, age_filter, price_filter): 
    df_filtered = df[df['house_age'].between(age_filter[0], age_filter[1]) & df['SalePrice'].between(price_filter[0], price_filter[1])]
    fig = px.scatter(df_filtered, x='house_age', y='SalePrice')
    st.plotly_chart(fig)


def main():
    '''
    run with the following command in the command line
    python -m streamlit run <insert path to python script>
    '''
    df = load_and_filter_data()
    age_filter = create_slider(df, column="house_age", label="House Age")
    price_filter = create_slider(df, column="SalePrice", label="Sale Price")
    sale_price_scatter(df, age_filter, price_filter) 
    
main()