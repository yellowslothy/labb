import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Virus Grid Simulator")
st.title("🧍‍♂️ Virus Spread Grid Simulator")
st.markdown("""
Each dot represents a person. Red = Infected, Green = Healthy, Blue = Recovered, Black = Dead.
Watch the virus spread over time!
""")

grid_size = st.sidebar.slider("Grid Size (N x N)", 10, 100, 30)
infection_radius = st.sidebar.slider("Infection Radius", 1, 5, 1)
infection_chance = st.sidebar.slider("Infection Chance (%)", 0, 100, 20)
recovery_time = st.sidebar.slider("Recovery Time (steps)", 5, 30, 10)
mortality_rate = st.sidebar.slider("Mortality Rate (%)", 0, 100, 5)

grid = np.zeros((grid_size, grid_size), dtype=int)
timers = np.zeros_like(grid)

center = grid_size // 2
grid[center, center] = 1

plot_area = st.empty()

if st.button("Reset Simulation"):
    st.experimental_rerun()

for step in range(100):
    new_grid = grid.copy()
    new_timers = timers.copy()

    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i, j] == 1:
                new_timers[i, j] += 1
                for dx in range(-infection_radius, infection_radius + 1):
                    for dy in range(-infection_radius, infection_radius + 1):
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < grid_size and 0 <= nj < grid_size:
                            if grid[ni, nj] == 0 and np.random.rand() < infection_chance / 100:
                                new_grid[ni, nj] = 1
                if new_timers[i, j] >= recovery_time:
                    if np.random.rand() < mortality_rate / 100:
                        new_grid[i, j] = 3
                    else:
                        new_grid[i, j] = 2

    grid = new_grid
    timers = new_timers

    color_map = {0: [0.2, 0.8, 0.2], 1: [1, 0, 0], 2: [0.2, 0.2, 1], 3: [0, 0, 0]}
    rgb_grid = np.zeros((grid_size, grid_size, 3))
    for state, color in color_map.items():
        rgb_grid[grid == state] = color

    fig, ax = plt.subplots()
    ax.imshow(rgb_grid, interpolation='none')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"Step {step + 1}")
    plot_area.pyplot(fig)
    time.sleep(0.2)

st.markdown("""
**Legend:**
- 🟢 Green: Healthy
- 🔴 Red: Infected
- 🔵 Blue: Recovered
- ⚫️ Black: Dead
""")
