import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.title("📊 Disagreement Analysis Dashboard")
st.write("Analysis of 'Strongly Disagree' and 'Disagree' responses across all Likert items.")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_data.csv")

df = load_data()

# Identify Columns
likert_cols = [col for col in df.columns if any(x in col for x in ['Factor', 'Effect', 'Step'])]
factor_cols = [col for col in likert_cols if 'Factor' in col]
effect_cols = [col for col in likert_cols if 'Effect' in col]
step_cols   = [col for col in likert_cols if 'Step' in col]

# --- PRE-PROCESSING DATA ---
heatmap_data = []
for area in ['Rural areas', 'Suburban areas', 'Urban areas']:
    for col in likert_cols:
        sd = (df[df['Area Type'] == area][col] == 1).sum()
        d  = (df[df['Area Type'] == area][col] == 2).sum()
        total = sd + d
        if total > 0:
            category = 'Factor' if col in factor_cols else 'Effect' if col in effect_cols else 'Step'
            heatmap_data.append({
                'Area Type': area, 'Likert Item': col, 'Total': total,
                'SD': sd, 'D': d, 'Category': category
            })

h_df = pd.DataFrame(heatmap_data)
pivot_z = h_df.pivot(index='Likert Item', columns='Area Type', values='Total').fillna(0)

# --- DASHBOARD TABS ---
tab1, tab2, tab3 = st.tabs(["🔥 Heatmap Analysis", "📊 Bar Chart Ranking", "📋 Summary Table"])

with tab1:
    st.subheader("Interactive Disagreement Heatmap")
    
    # Custom Data for Hover
    pivot_sd = h_df.pivot(index='Likert Item', columns='Area Type', values='SD').fillna(0)
    pivot_d = h_df.pivot(index='Likert Item', columns='Area Type', values='D').fillna(0)
    
    custom_data = np.stack([pivot_sd.values, pivot_d.values], axis=-1)

    fig_heat = go.Figure(data=go.Heatmap(
        z=pivot_z.values, x=pivot_z.columns, y=pivot_z.index,
        colorscale='YlGnBu', customdata=custom_data,
        hovertemplate='<b>%{y}</b><br>Area: %{x}<br>Total: %{z}<br>SD: %{customdata[0]}<br>D: %{customdata[1]}<extra></extra>'
    ))
    st.plotly_chart(fig_heat, use_container_width=True)

with tab2:
    st.subheader("Total Disagreement Ranking")
    summary_df = pivot_z.copy()
    summary_df['Total'] = summary_df.sum(axis=1)
    summary_df = summary_df.sort_values('Total', ascending=True).reset_index()

    fig_bar = px.bar(
        summary_df, x='Total', y='Likert Item', orientation='h',
        title="Items with Highest Disagreement",
        color='Total', color_continuous_scale='Reds'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with tab3:
    st.subheader("Raw Data Breakdown")
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    st.download_button("Download CSV", summary_df.to_csv(index=False), "disagreement_summary.csv")
