import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide")
st.title("🦠 Virus Spread Simulation on Map")

grid_size = st.slider("Grid Size", 5, 20, 10)
spread_chance = st.slider("Infection Rate (%)", 0, 100, 30)
city_center = {"lat": 37.5665, "lon": 126.9780}  # 서울 중심

HEALTHY, INFECTED, RECOVERED, DEAD = 0, 1, 2, 3
status_colors = {HEALTHY: "green", INFECTED: "red", RECOVERED: "blue", DEAD: "black"}

if "grid" not in st.session_state:
    st.session_state.grid = np.zeros((grid_size, grid_size), dtype=int)
    mid = grid_size // 2
    st.session_state.grid[mid, mid] = INFECTED
    st.session_state.step = 0

def spread(grid):
    new_grid = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == INFECTED:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < grid.shape[0] and 0 <= nj < grid.shape[1]:
                            if grid[ni, nj] == HEALTHY and np.random.rand() < spread_chance / 100:
                                new_grid[ni, nj] = INFECTED
                new_grid[i, j] = RECOVERED
    return new_grid

lat_range = np.linspace(city_center["lat"] - 0.05, city_center["lat"] + 0.05, grid_size)
lon_range = np.linspace(city_center["lon"] - 0.05, city_center["lon"] + 0.05, grid_size)
lats, lons, colors = [], [], []

for i in range(grid_size):
    for j in range(grid_size):
        lats.append(lat_range[i])
        lons.append(lon_range[j])
        colors.append(status_colors[st.session_state.grid[i, j]])

df = pd.DataFrame({"lat": lats, "lon": lons, "color": colors})

fig = go.Figure(go.Scattermapbox(
    lat=df["lat"],
    lon=df["lon"],
    mode="markers",
    marker=dict(size=14, color=df["color"]),
    hoverinfo="none"
))

fig.update_layout(
    mapbox_style="open-street-map",
    mapbox=dict(center=city_center, zoom=12),
    margin=dict(l=0, r=0, t=0, b=0),
    height=650
)

st.plotly_chart(fig)

if st.session_state.step < 20:
    time.sleep(1)
    st.session_state.grid = spread(st.session_state.grid)
    st.session_state.step += 1
    st.experimental_rerun()
else:
    st.success("Simulation Complete ✅")

st.markdown("""
### 🧬 Legend
- 🟢 Healthy  
- 🔴 Infected  
- 🔵 Recovered  
""")
