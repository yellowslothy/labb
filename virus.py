import streamlit as st
import numpy as np
from PIL import Image

st.title("🦠 Virus Spread Simulation (Image Grid Version)")

grid_size = st.slider("Grid Size", 10, 30, 20)
spread_chance = st.slider("Infection Rate (%)", 0, 100, 30)
max_steps = st.slider("Max Steps", 1, 50, 20)

HEALTHY, INFECTED, RECOVERED = 0, 1, 2

colors = {
    HEALTHY: (0, 255, 0),      
    INFECTED: (255, 0, 0),    
    RECOVERED: (0, 0, 255)    
}

if 'grid' not in st.session_state or st.session_state.get('grid_size', 0) != grid_size:
    st.session_state.grid = np.zeros((grid_size, grid_size), dtype=int)
    mid = grid_size // 2
    st.session_state.grid[mid, mid] = INFECTED
    st.session_state.step = 0
    st.session_state.grid_size = grid_size

def spread(grid):
    new_grid = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == INFECTED:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < grid.shape[0] and 0 <= nj < grid.shape[1]:
                            if grid[ni, nj] == HEALTHY:
                                if np.random.rand() < spread_chance / 100:
                                    new_grid[ni, nj] = INFECTED
                new_grid[i, j] = RECOVERED
    return new_grid

def grid_to_image(grid):
    img = np.zeros((grid.shape[0], grid.shape[1], 3), dtype=np.uint8)
    for status, color in colors.items():
        img[grid == status] = color
    img = np.kron(img, np.ones((20, 20, 1))) 
    return Image.fromarray(img)

if st.session_state.step < max_steps:
    if st.button("Next Step"):
        st.session_state.grid = spread(st.session_state.grid)
        st.session_state.step += 1
else:
    st.success("Simulation Complete!")

img = grid_to_image(st.session_state.grid)
st.image(img, caption=f"Step {st.session_state.step}", use_column_width=False)

st.markdown("""
### 🧬 Legend
- 🟢 Healthy  
- 🔴 Infected  
- 🔵 Recovered  
""")
