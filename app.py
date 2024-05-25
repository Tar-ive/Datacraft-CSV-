import streamlit as st
import toml
from csv_analyzer.helpers import (
    load_data,
    display_data_preview,
    display_basic_statistics,
    display_data_types,
    display_missing_values,
    display_correlation_matrix,
    display_distribution_plots,
    display_line_chart,
    display_bar_chart,
    display_box_plot,
    clean_data,
    filter_data,
    generate_summary_report,
    display_welcome,
    display_trend_analysis,
)

# Load configuration from config.toml
config = toml.load("csv_analyzer/config.toml")

# Set page config with favicon
st.set_page_config(page_title="DataCraft CSV", page_icon="prompthero-prompt-ff9bdc63ada.png", layout="wide")

# Apply custom CSS from the configuration file
st.markdown(f"""
    <style>
    {config['css']['sidebar']}
    {config['css']['main']}
    </style>
""", unsafe_allow_html=True)

# Main function to display the app
def main():
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    
    st.sidebar.title("CSV File Analyzer")
    st.sidebar.write("Upload a CSV file to perform EDA")

    # Upload CSV file
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        data = load_data(uploaded_file)
        if data is not None:
            if st.sidebar.button("Preview Data"):
                st.session_state.page = "Preview"
            if st.sidebar.button("Overview"):
                st.session_state.page = "Overview"
            if st.sidebar.button("Data Types"):
                st.session_state.page = "Data Types"
            if st.sidebar.button("Missing Values"):
                st.session_state.page = "Missing Values"
            if st.sidebar.button("Correlation Matrix and Heatmap"):
                st.session_state.page = "Correlation Matrix and Heatmap"
            if st.sidebar.button("Distribution Plots"):
                st.session_state.page = "Distribution Plots"
            if st.sidebar.button("Line Chart"):
                st.session_state.page = "Line Chart"
            if st.sidebar.button("Bar Chart"):
                st.session_state.page = "Bar Chart"
            if st.sidebar.button("Box Plot"):
                st.session_state.page = "Box Plot"
            if st.sidebar.button("Data Cleaning"):
                st.session_state.page = "Data Cleaning"
            if st.sidebar.button("Custom Queries"):
                st.session_state.page = "Custom Queries"
            if st.sidebar.button("Summary Report"):
                st.session_state.page = "Summary Report"
            if st.sidebar.button("Trend Analysis"):
                st.session_state.page = "Trend Analysis"
            
            if st.session_state.page == "Preview":
                display_data_preview(data)
            elif st.session_state.page == "Overview":
                display_basic_statistics(data)
            elif st.session_state.page == "Data Types":
                display_data_types(data)
            elif st.session_state.page == "Missing Values":
                display_missing_values(data)
            elif st.session_state.page == "Correlation Matrix and Heatmap":
                display_correlation_matrix(data)
            elif st.session_state.page == "Distribution Plots":
                display_distribution_plots(data)
            elif st.session_state.page == "Line Chart":
                display_line_chart(data)
            elif st.session_state.page == "Bar Chart":
                display_bar_chart(data)
            elif st.session_state.page == "Box Plot":
                display_box_plot(data)
            elif st.session_state.page == "Data Cleaning":
                cleaned_data = clean_data(data)
                st.write("## Cleaned Data")
                st.dataframe(cleaned_data)
            elif st.session_state.page == "Custom Queries":
                filter_data(data)
            elif st.session_state.page == "Summary Report":
                generate_summary_report(data)
            elif st.session_state.page == "Trend Analysis":
                display_trend_analysis(data)
        else:
            st.error("Failed to load data. Please check the file format.")
    else:
        if st.session_state.page == "Home":
            display_welcome(config["welcome_image"]["path"])

if __name__ == "__main__":
    main()
