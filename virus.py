import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Virus Spread Simulator", layout="centered")
st.title("🦠 Virus Spread Simulator")
st.markdown("""
This simulator shows how a virus spreads in a population over time,
including the number of infected, recovered, and deceased individuals.
""")

st.sidebar.header("📊 Simulation Settings")
population = st.sidebar.number_input("Total Population", min_value=1000, value=10000, step=1000)
initial_infected = st.sidebar.slider("Initial Infected", 1, population // 2, 10)
r0 = st.sidebar.slider("Infection Rate (R₀)", 0.5, 5.0, 2.0, step=0.1)
mortality_rate = st.sidebar.slider("Mortality Rate (%)", 0.0, 20.0, 2.0, step=0.5)
recovery_days = st.sidebar.slider("Average Recovery Days", 5, 30, 14)
days = st.sidebar.slider("Simulation Duration (days)", 10, 180, 60)

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
ax.plot(S, label="Susceptible (S)", color="skyblue")
ax.plot(I, label="Infected (I)", color="orange")
ax.plot(R, label="Recovered (R)", color="green")
ax.plot(D, label="Deceased (D)", color="red")
ax.set_xlabel("Days")
ax.set_ylabel("Number of People")
ax.set_title("📈 Virus Spread Over Time")
ax.legend()
st.pyplot(fig)

st.subheader("📌 Summary")
st.write(f"**Total Infected:** {int(R[-1] + D[-1])} people")
st.write(f"**Total Recovered:** {int(R[-1])} people")
st.write(f"**Total Deceased:** {int(D[-1])} people")
