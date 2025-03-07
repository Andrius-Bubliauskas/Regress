import numpy as np
import plotly.graph_objects as go
import streamlit as st
from scipy.stats import linregress

# Streamlit app title
st.title("Interactive Linear Regression Analysis")

# User input for compound names
compounds = st.text_area("Enter compound names (comma-separated):", "CTM CMPD 8, CMPD 2, CMPD 1, CMPD 5, CMPD 6, CMPD 7")
compounds = [c.strip() for c in compounds.split(",")]

# User input for series names
series_1_name = st.text_input("Enter name for Series 1:", "1.7 µm Kinetex Evo C18 2.1 x 50 mm")
series_2_name = st.text_input("Enter name for Series 2:", "5 µm Gemini c18 21.2 x 150 mm")

# User input for series data
series_1 = st.text_area("Enter Series 1 (Analytical) retention times (comma-separated):", "0.144, 1.031, 1.096, 1.107, 1.22, 1.212")
series_1 = np.array([float(x.strip()) for x in series_1.split(",")])

series_2 = st.text_area("Enter Series 2 (Preparative) retention times (comma-separated):", "1.67, 5.17, 5.4, 5.23, 5.58, 5.33")
series_2 = np.array([float(x.strip()) for x in series_2.split(",")])

# Ensure input validity
if len(compounds) == len(series_1) == len(series_2):
    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = linregress(series_1, series_2)
    st.write(f"R-squared: {r_value**2:.4f}")

    # --- Plot 1: Retention times of analytes ---
    trace_1 = go.Scatter(
        x=compounds, 
        y=series_1, 
        mode='markers+text', 
        name=series_1_name,
        marker=dict(color='blue', size=10),
        text=[f'{series_1[i]:.2f}' for i in range(len(compounds))],
        textposition='bottom center'
    )

    trace_2 = go.Scatter(
        x=compounds, 
        y=series_2, 
        mode='markers+text', 
        name=series_2_name,
        marker=dict(color='red', size=10),
        text=[f'{series_2[i]:.2f}' for i in range(len(compounds))],
        textposition='top center'
    )

    layout_1 = go.Layout(
        title="Retention times of analytes",
        xaxis=dict(title="Compounds"),
        yaxis=dict(title="Retention time (min)"),
        showlegend=True
    )

    fig_1 = go.Figure(data=[trace_1, trace_2], layout=layout_1)
    st.plotly_chart(fig_1)

    # --- Plot 2: Linear Fit between Two Time Series ---
    fitted_line = go.Scatter(
        x=series_1, 
        y=slope * series_1 + intercept, 
        mode='lines', 
        name=f'Fitted Line: y = {slope:.2f}x + {intercept:.2f}',
        line=dict(color='blue', dash='dash')
    )

    trace_cmpd = go.Scatter(
        x=series_1, 
        y=series_2, 
        mode='markers+text', 
        name='CMPD',
        marker=dict(color='red', size=10),
        text=[f'{compounds[i]}' for i in range(len(compounds))],
        textposition='top center'
    )

    layout_2 = go.Layout(
        title="Linear Fit between Two Time Series",
        xaxis=dict(title="Analytical"),
        yaxis=dict(title="Preparative"),
        showlegend=True
    )

    fig_2 = go.Figure(data=[trace_cmpd, fitted_line], layout=layout_2)
    st.plotly_chart(fig_2)

else:
    st.error("Error: Ensure that all input fields have the same number of values.")
