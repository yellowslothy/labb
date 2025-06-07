import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from streamlit_autorefresh import st_autorefresh

st.title("🦠 Global Virus Spread Simulation")

infection_rate = st.slider("Infection Rate (%)", 0, 100, 30) / 100
death_rate = st.slider("Death Rate (%)", 0, 100, 5) / 100

data = {
    "city": ["Seoul", "New York", "London", "Tokyo", "Paris", "Sydney", "Cairo", "Moscow", "Rio de Janeiro", "Toronto"],
    "lat": [37.5665, 40.7128, 51.5074, 35.6895, 48.8566, -33.8688, 30.0444, 55.7558, -22.9068, 43.6532],
    "lon": [126.9780, -74.0060, -0.1278, 139.6917, 2.3522, 151.2093, 31.2357, 37.6173, -43.1729, -79.3832],
    "status": [0]*10 
}

df = pd.DataFrame(data)

if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.status = [0]*len(df)
    initially_infected = np.random.choice(len(df), size=2, replace=False)
    for idx in initially_infected:
        st.session_state.status[idx] = 1

count = st_autorefresh(interval=1000, limit=30, key="refresh")

def spread_virus(status_list, infection_rate, death_rate):
    new_status = status_list.copy()
    for i, s in enumerate(status_list):
        if s == 1:
            for j in range(len(status_list)):
                if status_list[j] == 0:
                    if np.random.rand() < infection_rate:
                        new_status[j] = 1
            if np.random.rand() < death_rate:
                new_status[i] = 3
            else:
                if np.random.rand() < 0.1:
                    new_status[i] = 2
    return new_status

if st.session_state.step < 30:
    st.session_state.status = spread_virus(st.session_state.status, infection_rate, death_rate)
    st.session_state.step += 1

colors = {0: "green", 1: "red", 2: "blue", 3: "black"}
df['status'] = st.session_state.status
df['color'] = df['status'].map(colors)

fig = px.scatter_geo(df,
                     lat='lat',
                     lon='lon',
                     hover_name='city',
                     color='color',
                     size=[20]*len(df),
                     projection="natural earth",
                     title=f"Global Spread - Step {st.session_state.step}")

fig.update_layout(legend_title_text='Status')

st.plotly_chart(fig, use_container_width=True)

if st.session_state.step >= 30:
    st.success("Simulation complete!")

st.markdown("""
---
### Legend
- 🟢 Green: Healthy  
- 🔴 Red: Infected  
- 🔵 Blue: Recovered  
- ⚫ Black: Dead
""")
