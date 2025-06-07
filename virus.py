import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import time

st.set_page_config(layout="wide")
st.title("🦠 Global Virus Spread Simulation")

infection_rate = st.slider("Infection Rate (%)", 0, 100, 30) / 100
death_rate = st.slider("Death Rate (%)", 0, 100, 5) / 100

data = {
    "city": ["Seoul", "New York", "London", "Tokyo", "Paris", "Sydney", "Cairo", "Moscow", "Rio", "Toronto"],
    "lat": [37.5665, 40.7128, 51.5074, 35.6895, 48.8566, -33.8688, 30.0444, 55.7558, -22.9068, 43.6532],
    "lon": [126.9780, -74.0060, -0.1278, 139.6917, 2.3522, 151.2093, 31.2357, 37.6173, -43.1729, -79.3832],
    "status": [0]*10
}

df = pd.DataFrame(data)

if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.status = [0]*len(df)
    initially_infected = np.random.choice(len(df), size=1, replace=False)
    for idx in initially_infected:
        st.session_state.status[idx] = 1

def spread_virus(status_list, infection_rate, death_rate):
    new_status = status_list.copy()
    for i, s in enumerate(status_list):
        if s == 1:
            for j in range(len(status_list)):
                if status_list[j] == 0 and np.random.rand() < infection_rate:
                    new_status[j] = 1
            if np.random.rand() < death_rate:
                new_status[i] = 3
            elif np.random.rand() < 0.15:
                new_status[i] = 2
    return new_status

status_icon = {
    0: "🟢 Healthy",
    1: "🔴 Infected",
    2: "🔵 Recovered",
    3: "⚫ Dead"
}

colors = {
    0: "limegreen",
    1: "crimson",
    2: "dodgerblue",
    3: "black"
}

sizes = {
    0: 10,
    1: 20,
    2: 15,
    3: 12
}

MAX_STEPS = 30

# 감염 확산
if st.session_state.step < MAX_STEPS:
    time.sleep(1)  # animation 효과
    st.session_state.status = spread_virus(st.session_state.status, infection_rate, death_rate)
    st.session_state.step += 1
    st.experimental_rerun()

df['status'] = st.session_state.status
df['color'] = df['status'].map(colors)
df['size'] = df['status'].map(sizes)
df['label'] = [f"{city} - {status_icon[status]}" for city, status in zip(df['city'], df['status'])]

fig = px.scatter_geo(df,
                     lat='lat',
                     lon='lon',
                     hover_name='label',
                     color='color',
                     size='size',
                     projection="natural earth",
                     title=f"🌍 Global Spread - Step {st.session_state.step}")

fig.update_layout(legend_title_text='Status', geo=dict(showland=True, landcolor="whitesmoke"))

st.plotly_chart(fig, use_container_width=True)

if st.session_state.step >= MAX_STEPS:
    st.success("✅ Simulation Complete")

st.markdown("""
---
### 🧭 Legend  
- 🟢 Healthy  
- 🔴 Infected  
- 🔵 Recovered  
- ⚫ Dead  
""")
