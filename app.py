import streamlit as st

st.set_page_config(
    page_title="School Traffic Analysis",
    page_icon="🚦",
    layout="wide"
)

# Define the pages
pg1 = st.Page("pages/Disagreement_Traffic.py", title="Disagreement Analysis", icon="📊")
pg2 = st.Page("pages/Izzati.py", title="Rural Perspectives", icon="🏘️")
pg3 = st.Page("pages/Fathin.py", title="Urban Perspectives", icon="🏙️")
pg4 = st.Page("pages/Khalida.py", title="Suburban Perspectives", icon="🏡")

# Initialize Navigation
pg = st.navigation([pg1, pg2, pg3, pg4])
pg.run()
