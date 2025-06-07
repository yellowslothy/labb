import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="centered")
st.title("🦠 City-Level Virus Spread Simulation")

city = st.selectbox("Select a City", ["Seoul", "New York", "London", "Tokyo", "Paris"])

infection_rate = st.slider("Infection Rate (%)", 0, 100, 20) / 100
death_rate = st.slider("Death Rate (%)", 0, 100, 5) / 100

grid_size = 20
if "grid" not in st.session_state or st.button("Restart Simulation"):
    st.session_state.grid = np.zeros((grid_size, grid_size), dtype=int)
    infected_index = np.random.randint(0, grid_size), np.random.randint(0, grid_size)
    st.session_state.grid[infected_index] = 1
    st.session_state.step = 0

def update_grid(grid):
    new_grid = grid.copy()
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i, j] == 1:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < grid_size and 0 <= nj < grid_size:
                            if grid[ni, nj] == 0 and np.random.rand() < infection_rate:
                                new_grid[ni, nj] = 1
                if np.random.rand() < death_rate:
                    new_grid[i, j] = 3
                elif np.random.rand() < 0.1:
                    new_grid[i, j] = 2
    return new_grid

placeholder = st.empty()  

steps = 30
for _ in range(steps):
    st.session_state.grid = update_grid(st.session_state.grid)
    st.session_state.step += 1

    fig, ax = plt.subplots()
    cmap = plt.cm.get_cmap("viridis", 4)
    ax.imshow(st.session_state.grid, cmap=cmap, vmin=0, vmax=3)
    ax.set_title(f"{city} - Step {st.session_state.step}")
    ax.axis("off")
    placeholder.pyplot(fig) 
    time.sleep(0.2)

st.markdown("""
---
### 🧭 Legend  
- 0 (Yellow-Green): Healthy  
- 1 (Blue): Infected  
- 2 (Light Purple): Recovered  
- 3 (Dark Purple): Dead  
""")
