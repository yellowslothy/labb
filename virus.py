import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from streamlit_autorefresh import st_autorefresh

st.title("🦠 Virus Spread on World Map")

infection_rate = st.slider("Infection Rate (%)", 0, 100, 50) / 100
death_rate = st.slider("Death Rate (%)", 0, 100, 10) / 100

data = {
    "city": ["Seoul", "New York", "London", "Tokyo", "Paris"],
    "lat": [37.5665, 40.7128, 51.5074, 35.6895, 48.8566],
    "lon": [126.9780, -74.0060, -0.1278, 139.6917, 2.3522],
    "status": [0]*5
}

df = pd.DataFrame(data)

start_city = st.selectbox("Select Patient Zero City:", df['city'])

if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.start_city = start_city
    st.session_state.status = [0]*5
    patient_zero_idx = df.index[df['city'] == start_city][0]
    st.session_state.status[patient_zero_idx] = 1

if start_city != st.session_state.start_city:
    st.session_state.step = 0
    st.session_state.start_city = start_city
    st.session_state.status = [0]*5
    patient_zero_idx = df.index[df['city'] == start_city][0]
    st.session_state.status[patient_zero_idx] = 1

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
                     title=f"Step {st.session_state.step}")

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
