import streamlit as st

st.set_page_config(
    page_title="Traffic Congestion Dashboard",
    layout="wide"
)

# Changed folder path from "pages/..." to "page/..."
pg1 = st.Page("page/Disagreement_Traffic.py", title="Disagreement Analysis", icon="📊")
pg2 = st.Page("page/Izzati.py", title="Rural Perspectives", icon="🏘️")
pg3 = st.Page("page/Fathin.py", title="Urban Perspectives", icon="🏙️")
pg4 = st.Page("page/Khalida.py", title="Suburban Perspectives", icon="🏡")

# Navigation
pg = st.navigation([pg1, pg2, pg3, pg4])
pg.run()
