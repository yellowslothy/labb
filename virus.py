import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.title("🦠 Virus Spread on World Map")

data = {
    "city": ["Seoul", "New York", "London", "Tokyo", "Paris"],
    "lat": [37.5665, 40.7128, 51.5074, 35.6895, 48.8566],
    "lon": [126.9780, -74.0060, -0.1278, 139.6917, 2.3522],
    "status": [0, 0, 0, 0, 0]  # 0: healthy, 1: infected, 2: recovered, 3: dead
}

df = pd.DataFrame(data)

start_city = st.selectbox("Select Patient Zero City:", df['city'])

if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.start_city = start_city

if start_city != st.session_state.start_city:
    st.session_state.step = 0
    st.session_state.start_city = start_city

def update_infection(step):
    infection_order = ["Seoul", "Tokyo", "New York", "London", "Paris"]
    if st.session_state.start_city in infection_order:
        infection_order.remove(st.session_state.start_city)
        infection_order = [st.session_state.start_city] + infection_order
    else:
        infection_order = [st.session_state.start_city] + infection_order

    if step < len(infection_order):
        city = infection_order[step]
        df.loc[df['city'] == city, 'status'] = 1

colors = {0: "green", 1: "red", 2: "blue", 3: "black"}
df['color'] = df['status'].map(colors)

update_infection(st.session_state.step)

fig = px.scatter_geo(df,
                     lat='lat',
                     lon='lon',
                     hover_name='city',
                     color='color',
                     size=[15]*len(df),
                     projection="natural earth")

fig.update_layout(title=f"Step {st.session_state.step + 1}",
                  legend_title_text='Status')

st.plotly_chart(fig)

if st.session_state.step < 4:
    time.sleep(1)
    st.session_state.step += 1
    st.experimental_rerun()
else:
    st.success("Simulation complete!")

st.markdown("""
---
### Legend
- 🟢 Green: Healthy  
- 🔴 Red: Infected  
- 🔵 Blue: Recovered  
- ⚫ Black: Dead
""")
