import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2
DEAD = 3

st.title("🦠 가상 바이러스 확산 시뮬레이터")

if "simulation_stats" not in st.session_state:
    st.session_state["simulation_stats"] = None
if "simulation_frames" not in st.session_state:
    st.session_state["simulation_frames"] = None
if "mode" not in st.session_state:
    st.session_state["mode"] = "animation"  


st.sidebar.header("바이러스 설정")
infection_rate = st.sidebar.slider("전염률", 0.0, 1.0, 0.2, 0.01)
fatality_rate = st.sidebar.slider("치명률", 0.0, 1.0, 0.05, 0.01)
initial_infected = st.sidebar.slider("초기 감염자 수", 1, 100, 10)
population_size = st.sidebar.slider("인구 격자 크기 (NxN)", 10, 100, 50)
days = st.sidebar.slider("시뮬레이션 일수", 1, 100, 50)
start_simulation = st.sidebar.button("시뮬레이션 시작")

def simulate(population_size, infection_rate, fatality_rate, initial_infected, days):
    grid = np.zeros((population_size, population_size), dtype=int)
    infected_indices = np.random.choice(population_size**2, initial_infected, replace=False)
    for idx in infected_indices:
        x, y = divmod(idx, population_size)
        grid[x, y] = INFECTED

    frames = [grid.copy()]
    stats = [
        (
            np.count_nonzero(grid == INFECTED),
            np.count_nonzero(grid == RECOVERED),
            np.count_nonzero(grid == DEAD),
        )
    ]

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

        infected = np.count_nonzero(new_grid == INFECTED)
        recovered = np.count_nonzero(new_grid == RECOVERED)
        dead = np.count_nonzero(new_grid == DEAD)
        stats.append((infected, recovered, dead))

        if np.array_equal(new_grid, grid) or infected == 0:
            frames.append(new_grid.copy())
            break

        grid = new_grid
        frames.append(grid.copy())

    return frames, stats

def display_animation(frames):
    colors = {
        SUSCEPTIBLE: [1, 1, 1],  
        INFECTED: [1, 0, 0],    
        RECOVERED: [0, 1, 0],    
        DEAD: [0.2, 0.2, 0.2]   
    }

    placeholder = st.empty()
    for day, frame in enumerate(frames):
        rgb_grid = np.zeros((frame.shape[0], frame.shape[1], 3))
        for state, color in colors.items():
            rgb_grid[frame == state] = color

        fig, ax = plt.subplots()
        ax.imshow(rgb_grid)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"Day {day + 1}")
        placeholder.pyplot(fig)
        time.sleep(0.1)

    st.markdown("---")
    st.markdown("### 🧾 상태 설명 (색상)")
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown("⬜️ 건강한 사람")
    col2.markdown("🟥 감염된 사람")
    col3.markdown("🟩 회복된 사람")
    col4.markdown("⬛️ 사망한 사람")

def show_graph(stats):
    stats = np.array(stats)
    days = np.arange(1, len(stats) + 1)

    fig, ax = plt.subplots()
    ax.plot(days, stats[:, 0], 'r-', label="감염자 수")
    ax.plot(days, stats[:, 1], 'g-', label="회복자 수")
    ax.plot(days, stats[:, 2], 'k-', label="사망자 수")

    ax.set_xlabel("일차")
    ax.set_ylabel("사람 수")
    ax.set_title("📊 일별 상태 변화")
    ax.legend()
    st.pyplot(fig)

if start_simulation:
    st.write("⏳ 시뮬레이션 진행 중...")
    frames, stats = simulate(population_size, infection_rate, fatality_rate, initial_infected, days)
    st.session_state["simulation_stats"] = stats
    st.session_state["simulation_frames"] = frames
    st.session_state["mode"] = "animation"
    st.success(f"✅ 시뮬레이션 완료! (총 {len(frames)}일 경과)")

if st.session_state["simulation_stats"] is not None and st.session_state["simulation_frames"] is not None:
    if st.session_state["mode"] == "animation":
        if st.button("📊 그래프로 보기"):
            st.session_state["mode"] = "graph"
    elif st.session_state["mode"] == "graph":
        if st.button("🎞️ 애니메이션으로 돌아가기"):
            st.session_state["mode"] = "animation"

if st.session_state["simulation_stats"] is not None and st.session_state["simulation_frames"] is not None:
    if st.session_state["mode"] == "animation":
        display_animation(st.session_state["simulation_frames"])
    elif st.session_state["mode"] == "graph":
        show_graph(st.session_state["simulation_stats"])
else:
    st.info("먼저 사이드바에서 '시뮬레이션 시작' 버튼을 눌러 시뮬레이션을 실행하세요.")
