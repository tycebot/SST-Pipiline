import streamlit as st
import pandas as pd
from ndbc_api import NdbcApi
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from datetime import datetime, timedelta
import plotly.graph_objects as go
import io
import folium
from streamlit_folium import st_folium

# Initialize NDBC API
api = NdbcApi()

# Define buoy stations
BUOY_STATIONS = {
    'San Francisco (Farallons) Buoy': '46026',
    'Fort Point Buoy 1': 'FTPC1',
    'Fort Point Buoy 2': 'FPXC1',
    'Davis Point': 'DPXC1',
    'Caequinez Strait': 'CQUC1',
    'Half Moon Bay 1': '46012',
    'Half Moon Bay 2': '1801589',
    'Point Reyes Buoy': 'PRYC1',
    'Monterey Bay Buoy': '46042',
    'San Francisco Bar Buoy': '46237',
    'Trinidad Pier Buoy': 'TDPC1'
    
}
Buoy_Coordinates={
    'San Francisco (Farallons) Buoy': '37.75,-122.838',
    'Fort Point Buoy 1': '37.806,-122.466',
    'Fort Point Buoy 2': '37.807,-122.466',
    'Davis Point': '38.056,-122.264',
    'Caequinez Strait': '38.066,-122.230',
    'Half Moon Bay 1': '37.356,-122.881',
    'Half Moon Bay 2': '37.21,-122.88',
    'Point Reyes Buoy': '37.996,-122.977',
    'San Francisco Bar Buoy': '37.788,-122.634',
    'Monterey Bay Buoy': '36.785,-122.396',
    'Trinidad Pier Buoy': '41.055,-124.147'
}
def get_buoy_data(station_id, start_date, end_date):
    """Get buoy data from NDBC API"""
    # Get data from NDBC API
    data = api.get_data(station_id=station_id, start_time=start_date,mode='stdmet', end_time=end_date) 
    data=data.reset_index()
    return data
    

def create_map(station):
    # Get the buoy's coordinates from the dictionary
    lat, lon = map(float, Buoy_Coordinates[station].split(','))
    
    # Create a Folium map object
    m = folium.Map(location=[lat, lon], zoom_start=10)
    
    # Add a marker to the map to represent the buoy's location
    folium.Marker([lat, lon], popup=station).add_to(m)
    
    return m

def plot_buoy_data(df,station):
    """Plot buoy data"""
    fig = go.Figure(data=[go.Scatter(x=df['timestamp'], y=df['WTMP'], mode='lines', name='SST')])
    fig.update_layout(title=station+' SST over time', xaxis_title='Date', yaxis_title='SST (°C)')
    return fig
    
def static_plot(df,station):
    # Create matplotlib figure for static download
    fig_static, ax = plt.subplots()
    ax.plot(df['timestamp'], df['WTMP'], label='SST')
    ax.set_title(station + ' SST over time')
    ax.set_xlabel('Date')
    ax.set_ylabel('SST (°C)')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    return fig_static

 # Function to create and manage the plot buffer
def create_plot_buffer(df, station):
    fig = static_plot(df, station)
    buffer = io.BytesIO()
    try:
        fig.savefig(buffer, format='png', dpi=300)
        buffer.seek(0)
        return buffer.getvalue()
    finally:
        buffer.close()
        plt.close(fig)

def main():
    st.title("Buoy Data Visualization")
    
    # Create sidebar for inputs
    st.sidebar.header("Data Selection")
    
    # Buoy station selection
    station = st.sidebar.selectbox(
        "Select Buoy Station",
        list(BUOY_STATIONS.keys())
    )
    
    # Date range selection
    start_date = st.sidebar.date_input(
        "Start Date",
        datetime(2021, 1, 1)
    ).strftime('%Y-%m-%d')
    
    end_date = st.sidebar.date_input(
        "End Date",
        datetime(2025, 1, 1)
    ).strftime('%Y-%m-%d')
    
    # Cache the data
    @st.cache_data
    def get_cached_data(station_id, start_date, end_date):
        return get_buoy_data(station_id, start_date, end_date)
    
    # Cache the plot
    @st.cache_data
    def get_cached_plot(df, station):
        return plot_buoy_data(df, station)
    
    @st.cache_data
    def get_cached_map(station):
        return create_map(station)

    # Get data once and reuse
    df = get_cached_data(BUOY_STATIONS[station], start_date, end_date)

    
    
    # Main content area
    st.header("SST Graph")
    
    # Get and plot the data (using cached plot)
    fig = get_cached_plot(df, station)
    st.plotly_chart(fig)

    # Map
    st.header("Buoy location on map")

    # Get and plot the map (using cached map)
    m = get_cached_map(station)
    st_folium(m, width=800, height=400)

     # Map
    st.header("Data or Plot Download")
    #Download button for data
    st.download_button("Download Data", 
    df.to_csv(index=False), 
    file_name=station + '_' + start_date + '_to_' + end_date +
    '.csv')
    
    # Download button for static plot   
    st.download_button(
        label="Download Plot",
        data=create_plot_buffer(df, station),
        file_name=station + '.png')

if __name__ == "__main__":
    main()