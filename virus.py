import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.title("🦠 가상 바이러스 확산 시뮬레이터")

st.sidebar.header("바이러스 커스텀 설정")
infection_rate = st.sidebar.slider("전염률 (infection rate)", 0.0, 1.0, 0.2, 0.01)
fatality_rate = st.sidebar.slider("치명률 (fatality rate)", 0.0, 1.0, 0.05, 0.01)
initial_infected = st.sidebar.slider("초기 감염자 수", 1, 100, 10)
population_size = st.sidebar.slider("인구 수 (격자 크기: NxN)", 10, 100, 50)
days = st.sidebar.slider("시뮬레이션 일수", 1, 100, 50)
start_simulation = st.sidebar.button("시뮬레이션 시작")

SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2
DEAD = 3

def simulate(population_size, infection_rate, fatality_rate, initial_infected, days):
    grid = np.zeros((population_size, population_size), dtype=int)
    infected_indices = np.random.choice(population_size * population_size, initial_infected, replace=False)
    for idx in infected_indices:
        x, y = divmod(idx, population_size)
        grid[x, y] = INFECTED
    
    frames = []
    for _ in range(days):
        new_grid = grid.copy()
        for i in range(population_size):
            for j in range(population_size):
                if grid[i, j] == INFECTED:
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            ni, nj = i + dx, j + dy
                            if 0 <= ni < population_size and 0 <= nj < population_size:
                                if grid[ni, nj] == SUSCEPTIBLE and np.random.rand() < infection_rate:
                                    new_grid[ni, nj] = INFECTED
                    if np.random.rand() < fatality_rate:
                        new_grid[i, j] = DEAD
                    else:
                        new_grid[i, j] = RECOVERED
        grid = new_grid
        frames.append(grid.copy())
    return frames

def display_animation(frames):
    fig, ax = plt.subplots()
    colors = {
        SUSCEPTIBLE: [1, 1, 1],
        INFECTED: [1, 0, 0],
        RECOVERED: [0, 1, 0],
        DEAD: [0.2, 0.2, 0.2]
    }

    for frame in frames:
        rgb_grid = np.zeros((frame.shape[0], frame.shape[1], 3))
        for state, color in colors.items():
            rgb_grid[frame == state] = color
        ax.clear()
        ax.imshow(rgb_grid)
        ax.set_xticks([])
        ax.set_yticks([])
        st.pyplot(fig)
        time.sleep(0.1)

if start_simulation:
    st.write("⏳ 시뮬레이션 중...")
    frames = simulate(population_size, infection_rate, fatality_rate, initial_infected, days)
    display_animation(frames)
    st.success("✅ 시뮬레이션 완료!")
