import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")
st.title("🦠 Global Virus Spread Simulation")

st_autorefresh(interval=1000, limit=50, key="refresh")

infection_rate = st.slider("Infection Rate (%)", 0, 100, 30) / 100
death_rate = st.slider("Death Rate (%)", 0, 100, 5) / 100

cities = {
    "city": ["Seoul", "New York", "London", "Tokyo", "Paris"],
    "lat": [37.5665, 40.7128, 51.5074, 35.6895, 48.8566],
    "lon": [126.9780, -74.0060, -0.1278, 139.6917, 2.3522]
}
df = pd.DataFrame(cities)

if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.status = [0] * len(df)
    patient_zero = np.random.choice(len(df), 1)[0]
    st.session_state.status[patient_zero] = 1

def spread_virus(status_list):
    new_status = status_list.copy()
    for i, s in enumerate(status_list):
        if s == 1:  # infected
            for j in range(len(status_list)):
                if status_list[j] == 0 and np.random.rand() < infection_rate:
                    new_status[j] = 1
            if np.random.rand() < death_rate:
                new_status[i] = 3
            elif np.random.rand() < 0.1:
                new_status[i] = 2
    return new_status

if st.session_state.step < 50:
    st.session_state.status = spread_virus(st.session_state.status)
    st.session_state.step += 1

colors = {0: "green", 1: "red", 2: "blue", 3: "black"}
sizes = {0: 10, 1: 20, 2: 15, 3: 12}
df['status'] = st.session_state.status
df['color'] = df['status'].map(colors)
df['size'] = df['status'].map(sizes)

fig = px.scatter_geo(df,
                     lat='lat',
                     lon='lon',
                     color='color',
                     size='size',
                     projection="natural earth",
                     hover_name='city',
                     title=f"Step {st.session_state.step}")

fig.update_layout(geo=dict(showland=True, landcolor="whitesmoke"))
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
---
### 🧭 Legend  
- 🟢 Healthy  
- 🔴 Infected  
- 🔵 Recovered  
- ⚫ Dead  
""")
