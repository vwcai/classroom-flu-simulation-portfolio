# Classroom Flu Monte Carlo Simulation

This repository is a public portfolio version of a Monte Carlo simulation project that models flu transmission in a classroom under different immunity assumptions.

The project compares two outbreak scenarios over 5,000 simulation runs: one with no initial immunity and one with 50% initial immunity. It tracks susceptible, infected, and recovered students over time, along with epidemic duration and early infection counts.

## Portfolio Version Note

This public version focuses on the simulation design, implementation, and results. Original course materials and internal project documents are intentionally omitted.

## Highlights

- Implements a classroom epidemic simulation in Python
- Models weekday-only transmission and fixed recovery duration
- Runs 5,000 Monte Carlo simulations per scenario
- Compares outbreak trajectories under different initial immunity levels
- Exports expected accumulated infection counts to CSV

## Selected Findings

- With **0% initial immunity**, the mean epidemic duration is about **11.91 days**
- With **50% initial immunity**, the mean epidemic duration falls to about **6.45 days**
- Final expected accumulated infections drop from about **12.10** to about **2.90**
- Higher initial immunity reduces total infections, shortens outbreaks, and lowers early spread

## Repository Contents

- `classroom_flu_simulation.ipynb`: cleaned notebook with simulation workflow and outputs
- `utils.py`: simulation engine and plotting helpers
- `sim_1_expected_num_of_accumulated_infections.csv`: exported results for the first scenario
- `sim_2_expected_num_of_accumulated_infections.csv`: exported results for the second scenario
- `requirements.txt`: Python dependencies used in the project

## Local Reproduction

Install dependencies:

```bash
pip install -r requirements.txt
```

Then open:

- `classroom_flu_simulation.ipynb`

## Skills Demonstrated

- simulation modeling
- Monte Carlo analysis
- scientific Python workflows
- data visualization
- scenario comparison
- result interpretation
