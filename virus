import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="바이러스 퍼짐 시뮬레이터", layout="centered")
st.title("🦠 바이러스 퍼짐 시뮬레이터")
st.markdown("""
이 시뮬레이터는 가상의 바이러스가 사람들 사이에 퍼질 때,
감염자, 회복자, 사망자 수가 시간에 따라 어떻게 변화하는지 보여줍니다.
""")

st.sidebar.header("📊 시뮬레이션 설정")
population = st.sidebar.number_input("총 인구 수", min_value=1000, value=10000, step=1000)
initial_infected = st.sidebar.slider("초기 감염자 수", 1, population // 2, 10)
r0 = st.sidebar.slider("감염력 (R₀)", 0.5, 5.0, 2.0, step=0.1)
mortality_rate = st.sidebar.slider("치사율 (%)", 0.0, 20.0, 2.0, step=0.5)
recovery_days = st.sidebar.slider("회복까지 걸리는 평균 일수", 5, 30, 14)
days = st.sidebar.slider("시뮬레이션 기간 (일)", 10, 180, 60)

beta = r0 / recovery_days
mortality = mortality_rate / 100

S = [population - initial_infected]
I = [initial_infected]
R = [0]
D = [0]

for day in range(1, days + 1):
    new_infected = beta * S[-1] * I[-1] / population
    new_recovered = I[-1] / recovery_days
    new_deaths = new_recovered * mortality
    new_recovered -= new_deaths

    S.append(S[-1] - new_infected)
    I.append(I[-1] + new_infected - new_recovered - new_deaths)
    R.append(R[-1] + new_recovered)
    D.append(D[-1] + new_deaths)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(S, label="감염 가능자 (S)", color="skyblue")
ax.plot(I, label="감염자 (I)", color="orange")
ax.plot(R, label="회복자 (R)", color="green")
ax.plot(D, label="사망자 (D)", color="red")
ax.set_xlabel("일")
ax.set_ylabel("사람 수")
ax.set_title("📈 감염병 확산 시뮬레이션 결과")
ax.legend()
st.pyplot(fig)

st.subheader("📌 요약 결과")
st.write(f"**총 감염자 수:** {int(R[-1] + D[-1])}명")
st.write(f"**총 회복자 수:** {int(R[-1])}명")
st.write(f"**총 사망자 수:** {int(D[-1])}명")
