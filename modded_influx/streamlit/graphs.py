import streamlit as st
import pandas as pd
import io
import plotly.express as px


# Functions for Line Graphs
def display_line_graphs(data):
    if data:
        df = pd.read_csv(io.StringIO(data))
        st.write(df)

        columns_to_plot = ['people_inside', 'power']
        x_column = '_time'

        # Add 'People vs Power' Graph
        if 'people_inside' in df.columns and 'power' in df.columns:
            st.subheader("People vs Power")
            fig_people_vs_power = px.scatter(df, x='people_inside', y='power', title="People vs Power")
            fig_people_vs_power.update_xaxes(title='People')  # Update x-axis label
            fig_people_vs_power.update_yaxes(title='Power')  # Update y-axis label
            st.plotly_chart(fig_people_vs_power, use_container_width=True)
        else:
            st.warning("Columns 'people_inside' or 'power' not found in the DataFrame.")

        # Check for necessary columns
        if all(col in df.columns for col in columns_to_plot + ['_time']):
            st.subheader("People Inside and Power vs Time")
            fig = px.line(df, x='_time', y=columns_to_plot, title="People Inside and Power vs Time")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"Columns {', '.join(columns_to_plot)}, or '_time' not found in the DataFrame.")
