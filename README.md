# Classroom Flu Monte Carlo Simulation

This repository is a public portfolio version of a Monte Carlo simulation project that models flu transmission in a classroom under different immunity assumptions.

The analysis compares two outbreak scenarios over 5,000 simulation runs and tracks how initial immunity changes infection trajectories, epidemic duration, and total accumulated infections.

## Public Portfolio Note

This public version focuses on the simulation design, implementation, and results. Original course materials and internal project documents are intentionally omitted.

## Start Here

- `PROJECT_SUMMARY.md`: main case-study style overview
- `classroom_flu_simulation.ipynb`: selected simulation workflow
- `utils.py`: simulation engine and plotting helpers

## At a Glance

- Business question: how does initial immunity change outbreak size and duration in a closed, high-contact classroom setting?
- Methods: stochastic discrete-time individual-based SIR simulation with weekday-only transmission and 5,000 Monte Carlo runs per scenario
- Headline takeaway: moving from 0% to 50% initial immunity reduced mean outbreak duration from about 11.91 days to 6.45 days and final expected accumulated infections from about 12.10 to 2.90

## Repository Contents

- `classroom_flu_simulation.ipynb`: cleaned notebook with simulation workflow and outputs
- `PROJECT_SUMMARY.md`: concise case-study style summary for portfolio review
- `utils.py`: simulation engine and plotting helpers
- `sim_1_expected_num_of_accumulated_infections.csv`: exported results for the first scenario
- `sim_2_expected_num_of_accumulated_infections.csv`: exported results for the second scenario
- `requirements.txt`: Python dependencies used in the project

## Data Note

This repository includes selected outputs and code used to illustrate the simulation workflow. Original prompt materials and internal project documents are intentionally omitted.

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
