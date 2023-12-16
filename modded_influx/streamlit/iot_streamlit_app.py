from influx_handler import *
from homepage import *
from graphs import *
from statistics import * 

import streamlit as st
import io

def main():
    st.set_page_config(layout="wide")
    st.title('Real-time Data Visualization from InfluxDB')

    st.sidebar.markdown("<h1>Select Category</h1>", unsafe_allow_html=True)
    selected_category = st.sidebar.radio("", 
    ('Project Explanation','Historic Data Visualization', 'Real-time data Visualization'))

    data = None
    if selected_category == 'Project Explanation':
        display_project_explanation()
    elif selected_category == 'Historic Data Visualization':
        data = get_historic_data()
    elif selected_category == 'Real-time data Visualization':
        data = get_real_time_data()

    st.sidebar.markdown("<br><hr>", unsafe_allow_html=True) 

    st.sidebar.markdown(f"<h1>{selected_category} Sub-divisions</h1>", unsafe_allow_html=True)
    selected_subcategory = st.sidebar.radio("", ('Graphs', 'Statistics'))

    if selected_subcategory == 'Graphs':
        display_line_graphs(data)
    elif selected_subcategory == 'Statistics':
        display_statistics(data)

if __name__ == "__main__":
    main()