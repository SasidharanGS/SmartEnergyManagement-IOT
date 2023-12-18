import streamlit as st
import pandas as pd
import io
import plotly.express as px

# Function for Correlation
def display_correlation(data):
    if data.empty:
        st.warning("No data available to display correlation.")
    else:
        st.write(data)

        numeric_columns = data.select_dtypes(include=['float64', 'int64'])
        col1, col2 = st.multiselect("Select Columns for Correlation", numeric_columns.columns)

        if col1 and col2:
            selected_columns = [col1, col2]
            fig_corr = px.scatter(data, x=col1, y=col2, title=f"{col1.capitalize()} vs {col2.capitalize()} Correlation")
            fig_corr.update_xaxes(title=col1)  # Update x-axis label
            fig_corr.update_yaxes(title=col2)  # Update y-axis label
            st.plotly_chart(fig_corr, use_container_width=True)

            # Calculate correlation coefficient
            correlation_coefficient = data[selected_columns].corr().iloc[0, 1]
            st.info(f"Correlation Coefficient between {col1.capitalize()} and {col2.capitalize()}: {correlation_coefficient:.2f}")
        else:
            st.warning("Please select two columns for correlation.")


# Function for Statistics
def display_statistics(data):
    if data:
        df = pd.read_csv(io.StringIO(data))
        selected_columns = ['current', 'energy', 'frequency', 'people_inside', 'power']
        st.write(df[selected_columns])  # Displaying specific columns

        avg_values = df[selected_columns].mean()  # Calculate mean for selected columns
        st.subheader("Average Values")
        fig_avg = px.bar(x=avg_values.index, y=avg_values.values, labels={'x': 'Measurements', 'y': 'Average Values'})
        st.plotly_chart(fig_avg, use_container_width=True)

        st.subheader("Correlation Graph")
        display_correlation(df[selected_columns])  # Display correlation for selected columns
    else:
        st.error("Error retrieving data. Please check the connection or selected category.")
