# SST-Pipiline

A comprehensive sea surface temperature (SST) data analysis toolkit featuring a Streamlit visualization app and a complete ETL pipeline for multi-source oceanographic data integration. This project combines buoy data, satellite imagery, and in-situ logger measurements for comprehensive coastal temperature analysis.

## 🌊 [Live Demo - Try the App Now!](https://terrellbuoysst.streamlit.app)

Project Components
1. Streamlit Visualization App (app.py)

-Interactive Data Selection: Choose from 7 pre-configured buoy stations
-Custom Date Ranges: Select specific time periods for analysis
-Interactive Visualizations: Dynamic Plotly charts with zoom and hover capabilities
-Data Export: Download raw data as CSV files
-Plot Export: Download high-resolution PNG plots
-Performance Optimized: Built-in caching for faster data retrieval and plotting

2. SST Data Pipeline (SST Pipeline.ipynb)

-Multi-Source Integration: Combines NDBC buoy data, NOAA satellite data, and HOBO logger measurements
-Spatial Analysis: Defines and analyzes specific coastal sites with custom coordinate boundaries
-Interactive Mapping: Folium-based site visualization with Esri National Geographic tiles
-Data Fusion: Merges multiple data sources for comprehensive temperature analysis
