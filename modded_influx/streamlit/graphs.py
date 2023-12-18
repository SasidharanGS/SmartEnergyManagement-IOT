import streamlit as st
import pandas as pd
import io
import plotly.express as px
import plotly.graph_objects as go

hr = lambda: st.markdown("<hr>", unsafe_allow_html=True)

def graphs(data):
    if data:
        df = pd.read_csv(io.StringIO(data))
        df['_time'] = pd.to_datetime(df['_time'])  # Convert '_time' column to datetime
        st.write(df)
        hr()

        display_line_graphs(df)
        hr()
        display_power_by_day(df)
        hr()
        display_power_for_day(df)
        hr()
    else:
        st.warning("No data found or invalid data format")

def display_power_by_day(df):
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    df['_day_name'] = df['_time'].dt.day_name()  # Create a new column for day names
    avg_power_by_day = df.groupby('_day_name')['power'].mean().reindex(days)
    
    st.subheader("Power Consumption")
    fig = px.bar(x=avg_power_by_day.index, y=avg_power_by_day.values, title='Average Power Usage by Weekday')
    fig.update_layout(xaxis_title="Weekday", xaxis={'title_standoff': 20})
    fig.update_layout(yaxis_title="Watts", yaxis={'title_standoff': 20})
    st.plotly_chart(fig, use_container_width=True)

    most_power_day = avg_power_by_day.idxmax()
    st.markdown(f"<div style='text-align: center'><b><u>{most_power_day}</b></u> has the highest average power usage.</div>", unsafe_allow_html=True)

def display_power_for_day(df):
    st.subheader("Power vs Day Graph")
    df['_time'] = pd.to_datetime(df['_time'])
    df['period'] = df['_time'].apply(lambda x: 'Forenoon' if x.hour < 12 else 'Afternoon')
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['_day_name'] = df['_time'].dt.day_name()
    avg_df = df.groupby(['_day_name', 'period'])['power'].mean().unstack().reindex(days)  # Rearranging index here
    avg_df = avg_df.fillna(0)
    st.write(avg_df)
    st.line_chart(avg_df, height=600)   #this step somehow changes the index order  - have to rectify


def display_line_graphs(df):
    columns_to_plot = ['people_inside', 'power']
    x_column = '_time'
    # 'People vs Power' Graph
    if all(col in df.columns for col in columns_to_plot):
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
        fig.update_traces(line=dict(color='orange', width=2), selector=dict(name='power'))  # Setting power line color
        fig.update_traces(line=dict(color='blue', width=2), selector=dict(name='people_inside'))  # Setting people_inside line color
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"Columns {', '.join(columns_to_plot)}, or '_time' not found in the DataFrame.")

