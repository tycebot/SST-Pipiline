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
# Initialize NDBC API
api = NdbcApi()

# Define buoy stations
BUOY_STATIONS = {
    'Delaware Buoy': '44009',
    'Humboldt Buoy': '46244'
}

def get_buoy_data(station_id, start_date, end_date):
    """Get buoy data from NDBC API"""
    # Get data from NDBC API
    data = api.get_data(station_id=station_id, start_time=start_date,mode='stdmet', end_time=end_date) 
    data=data.reset_index()
    return data
    


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
        datetime(2020, 1, 1)
    ).strftime('%Y-%m-%d')
    
    end_date = st.sidebar.date_input(
        "End Date",
        datetime.now()
    ).strftime('%Y-%m-%d')
    
    # Cache the data
    @st.cache_data
    def get_cached_data(station_id, start_date, end_date):
        return get_buoy_data(station_id, start_date, end_date)
    
    # Cache the plot
    @st.cache_data
    def get_cached_plot(df, station):
        return plot_buoy_data(df, station)
    
    # Get data once and reuse
    df = get_cached_data(BUOY_STATIONS[station], start_date, end_date)

    # Main content area
    st.header("Buoy Data Visualization")
    
    # Get and plot the data (using cached plot)
    fig = get_cached_plot(df, station)
    st.plotly_chart(fig)

    
    # Retrieve the cached plot
    fig = get_cached_plot(df, station)
    statplot=static_plot(df,station)
    buffer = io.BytesIO()
    statplot.savefig(buffer, format='png',dpi=300)
    buffer.seek(0)

    #Download button for data
    st.download_button("Download Data", 
    df.to_csv(index=False), 
    file_name=station + 
    '.csv')
    
    # Download button for static plot   
    st.download_button(
        label="Download Plot",
        data=buffer,
        file_name=station + '.png')

if __name__ == "__main__":
    main()