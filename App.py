import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG (CLEAN LOOK)
# =========================
st.set_page_config(
    page_title="CO2 Dashboard",
    layout="wide",
    page_icon=""
)

st.title("CO₂ Emissions Dashboard")
st.markdown("### Clean & Interactive Data Visualization")

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_excel("cleaned_co2.xlsx")

# CLEAN COLUMN NAMES
df.columns = df.columns.astype(str).str.strip()

# REMOVE EMPTY COLUMNS
df = df.dropna(axis=1, how="all")

# ----------------------------
# SIDEBAR (LIKE YOUR FRIEND)
# ----------------------------
st.sidebar.header("Controls")

x_axis = st.sidebar.selectbox("Select X-axis", df.columns)
y_axis = st.sidebar.selectbox("Select Y-axis", df.columns)

# ----------------------------
# KPI SECTION (TOP CARDS)
# ----------------------------
st.markdown("---")
col1, col2, col3 = st.columns(3)

col1.metric("Rows", len(df))
col2.metric("Columns", len(df.columns))
col3.metric("Selected Column", y_axis)

st.markdown("---")

# ----------------------------
# MAIN CHART (BIG)
# ----------------------------
st.subheader("Main Visualization")

chart_type = st.selectbox(
    "Select Chart Type",
    ["Bar Chart", "Line Chart", "Scatter Plot"]
)

if chart_type == "Bar Chart":
    fig = px.bar(df, x=x_axis, y=y_axis, template="plotly_white")
elif chart_type == "Line Chart":
    fig = px.line(df, x=x_axis, y=y_axis, template="plotly_white")
else:
    fig = px.scatter(df, x=x_axis, y=y_axis, template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

# ----------------------------
st.subheader("Pie Chart (Top 10 Countries)")

# Find numeric + category columns
numeric_cols = df.select_dtypes(include="number").columns
category_cols = df.select_dtypes(include="object").columns

if len(numeric_cols) > 0 and len(category_cols) > 0:

    value_col = numeric_cols[0]
    name_col = category_cols[0]

    pie_data = (
        df.groupby(name_col)[value_col]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_pie = px.pie(
        pie_data,
        names=name_col,
        values=value_col
    )

    st.plotly_chart(fig_pie, use_container_width=True)

else:
    st.warning("No suitable data for pie chart")
# SECOND ROW (SIDE BY SIDE)
# ----------------------------
col4, col5 = st.columns(2)

# Histogram
with col4:
    st.subheader("Distribution")
    try:
        fig2 = px.histogram(df, x=y_axis, template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)
    except:
        st.warning("Cannot create histogram")

# Correlation
with col5:
    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] > 1:
        st.subheader("Correlation Heatmap")
        fig3 = px.imshow(numeric_df.corr(), text_auto=True)
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Not enough numeric columns")

# ----------------------------
st.subheader("Top 10 Values")

numeric_cols = df.select_dtypes(include="number").columns
category_cols = df.select_dtypes(include="object").columns

if len(numeric_cols) > 0 and len(category_cols) > 0:

    value_col = numeric_cols[0]
    name_col = category_cols[0]

    top10 = (
        df.groupby(name_col)[value_col]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_top = px.bar(
        top10,
        x=value_col,
        y=name_col,
        orientation="h"
    )

    st.plotly_chart(fig_top, use_container_width=True)

else:
    st.warning("Top 10 chart not possible")
# DATA TABLE
# ----------------------------
st.markdown("---")
st.subheader("Dataset Preview")
st.dataframe(df, use_container_width=True)
st.subheader("Trend Line")

try:
    fig_line2 = px.line(df, x=x_axis, y=y_axis)
    st.plotly_chart(fig_line2, use_container_width=True)
except:
    st.warning("Line chart not possible")
# ----------------------------
# FOOTER
# ----------------------------
st.success("Dashboard running successfully")