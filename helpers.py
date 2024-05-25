import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st
from statsmodels.tsa.seasonal import seasonal_decompose

def load_data(file_path):
    try:
        return pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        return pd.read_csv(file_path, encoding='ISO-8859-1')

def display_data_preview(data):
    st.write("## Data Preview")
    st.dataframe(data.head(20))

def display_basic_statistics(data):
    st.write("## Basic Statistics")
    st.write(data.describe())

def display_data_types(data):
    st.write("## Data Types")
    st.dataframe(data.dtypes.reset_index().rename(columns={"index": "Column", 0: "Data Type"}))

def display_missing_values(data):
    st.write("## Missing Values")
    st.dataframe(data.isnull().sum().reset_index().rename(columns={"index": "Column", 0: "Missing Values"}))

def display_correlation_matrix(data):
    numeric_data = data.select_dtypes(include=[float, int])
    st.write("## Correlation Matrix")
    if not numeric_data.empty:
        corr = numeric_data.corr()
        st.write(corr)
        
        st.write("## Correlation Heatmap")
        fig = ff.create_annotated_heatmap(
            z=corr.values,
            x=list(corr.columns),
            y=list(corr.index),
            annotation_text=corr.round(2).values,
            colorscale='Viridis'
        )
        fig.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font_color='white'
        )
        st.plotly_chart(fig)
    else:
        st.write("No numeric data available for correlation matrix.")

def display_distribution_plots(data):
    numeric_data = data.select_dtypes(include=[float, int])
    st.write("## Distribution Plots")
    for column in numeric_data.columns:
        st.write(f"### Distribution of {column}")
        fig = px.histogram(data, x=column, nbins=30, marginal="box", title=f"Distribution of {column}", height=400, width=600, color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font_color='white'
        )
        st.plotly_chart(fig)
        
        # Add insights
        mean_value = data[column].mean()
        median_value = data[column].median()
        std_dev = data[column].std()
        st.write(f"**Insights for {column}:**")
        st.write(f"- Mean: {mean_value:.2f}")
        st.write(f"- Median: {median_value:.2f}")
        st.write(f"- Standard Deviation: {std_dev:.2f}")
        st.write(f"**Interpretation:** The histogram shows the distribution of {column}. The mean value is {mean_value:.2f}, which indicates the central tendency of the data. The median value is {median_value:.2f}, which shows the middle point of the data. The standard deviation is {std_dev:.2f}, indicating the spread of the data around the mean.")

def display_line_chart(data):
    st.write("## Line Chart")
    numeric_data = data.select_dtypes(include=[float, int])
    for column in numeric_data.columns:
        fig = px.line(data, x=data.index, y=column, title=f"Line Chart of {column}", color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font_color='white'
        )
        st.plotly_chart(fig)

def display_bar_chart(data):
    st.write("## Bar Chart")
    numeric_data = data.select_dtypes(include=[float, int])
    for column in numeric_data.columns:
        fig = px.bar(data, x=data.index, y=column, title=f"Bar Chart of {column}", color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font_color='white'
        )
        st.plotly_chart(fig)

def display_box_plot(data):
    st.write("## Box Plot")
    numeric_data = data.select_dtypes(include=[float, int])
    for column in numeric_data.columns:
        fig = px.box(data, y=column, title=f"Box Plot of {column}", color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font_color='white'
        )
        st.plotly_chart(fig)

        # Add insights
        median_value = data[column].median()
        q1 = data[column].quantile(0.25)
        q3 = data[column].quantile(0.75)
        iqr = q3 - q1
        st.write(f"**Insights for {column}:**")
        st.write(f"- Median: {median_value:.2f}")
        st.write(f"- Q1 (25th percentile): {q1:.2f}")
        st.write(f"- Q3 (75th percentile): {q3:.2f}")
        st.write(f"- IQR (Interquartile Range): {iqr:.2f}")
        st.write(f"**Interpretation:** The box plot shows the distribution of {column}. The median value is {median_value:.2f}, which indicates the central value of the data. The interquartile range (IQR) is {iqr:.2f}, which measures the spread of the middle 50% of the data. The Q1 and Q3 values represent the 25th and 75th percentiles, respectively.")

def clean_data(data):
    st.write("## Data Cleaning")
    
    if st.checkbox("Drop missing values"):
        data = data.dropna()
    
    if st.checkbox("Drop duplicates"):
        data = data.drop_duplicates()

    return data

def filter_data(data):
    st.write("## Custom Queries")
    column = st.selectbox("Select Column", data.columns)
    st.write(f"Data Type: {data[column].dtype}")
    condition = st.text_input("Enter Condition (e.g., > 50)")
    if st.button("Apply Filter"):
        try:
            filtered_data = data.query(f"{column} {condition}")
            st.write(f"Filtered Data (Rows: {filtered_data.shape[0]})")
            st.dataframe(filtered_data)
        except Exception as e:
            st.error(f"Error: {e}")

def generate_summary_report(data):
    st.write("## Summary Report")
    st.write(data.describe())
    st.write("Missing Values")
    st.write(data.isnull().sum().reset_index().rename(columns={"index": "Column", 0: "Missing Values"}))
    numeric_data = data.select_dtypes(include=[float, int])
    if not numeric_data.empty:
        st.write("Correlation Matrix")
        st.write(numeric_data.corr())

def display_welcome(image_path):
    st.image(image_path, use_column_width=True)
    st.write("### Welcome to DataCraft CSV!")
    st.write("Upload your CSV file to get started and explore various data analysis features.")

def display_trend_analysis(data):
    st.write("## Trend Analysis")
    date_column = st.selectbox("Select Date Column", data.columns)
    if date_column:
        time_series_data = data.set_index(date_column)
        numeric_columns = time_series_data.select_dtypes(include=[float, int]).columns
        
        for column in numeric_columns:
            st.write(f"### Trend Analysis for {column}")
            time_series = time_series_data[column].dropna()
            result = seasonal_decompose(time_series, model='additive', period=1)
            
            fig = px.line(time_series, title=f"Time Series of {column}", color_discrete_sequence=px.colors.qualitative.Bold)
            fig.add_scatter(x=result.trend.index, y=result.trend, mode='lines', name='Trend')
            fig.add_scatter(x=result.seasonal.index, y=result.seasonal, mode='lines', name='Seasonal')
            fig.add_scatter(x=result.resid.index, y=result.resid, mode='lines', name='Residual')
            
            fig.update_layout(
                plot_bgcolor='#1e1e1e',
                paper_bgcolor='#1e1e1e',
                font_color='white'
            )
            
            st.plotly_chart(fig)
            
            st.write(f"**Insights for {column}:**")
            st.write(f"- The trend component shows the long-term movement in the data.")
            st.write(f"- The seasonal component shows the repeating short-term cycle in the data.")
            st.write(f"- The residual component is the remaining part after removing the trend and seasonality.")
