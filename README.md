# Classroom Flu Monte Carlo Simulation

This repository is a public portfolio version of a Monte Carlo simulation project that models flu transmission in a classroom under different immunity assumptions.

## Public Portfolio Note

This public version focuses on the simulation design, implementation, and results. Original course materials and internal project documents are intentionally omitted.

## Project Overview

This project uses Monte Carlo simulation to measure how a change in initial immunity affects outbreak size, timing, and duration in a closed, high-contact classroom setting.

## Business Problem

The broader business question is how much an upfront preventive condition can reduce downstream disruption. In operational settings, that kind of problem shows up in workforce planning, continuity management, and risk reduction: decision-makers want to know whether prevention meaningfully lowers disruption before a problem spreads.

## Data

- Source: scenario inputs defined in the simulation plus exported simulation outputs generated in Python
- Type: synthetic scenario data and simulated operational-risk outcomes
- Included here: selected CSV outputs and notebook-based analysis workflow
- Not included: original course prompt materials and internal project documents

## Approach

- Built a stochastic discrete-time individual-based SIR simulation in Python
- Modeled a classroom of 61 students with weekday-only transmission and a fixed recovery duration
- Ran 5,000 Monte Carlo iterations for each scenario
- Compared a `0%` immunity scenario with a `50%` immunity scenario
- Validated early infection counts against a simple analytical benchmark

## Key Insights

- Raising initial immunity from `0%` to `50%` reduced mean outbreak duration from about `11.91` days to `6.45` days
- Final expected accumulated infections fell from about `12.10` to `2.90`
- The higher-immunity scenario kept transmission under control earlier, which sharply reduced downstream disruption
- Small changes in starting conditions created large differences in total outcomes

## Recommendations

- If this were a real operational setting, I would prioritize preventive actions that improve the starting condition before disruption begins
- I would use scenario modeling to compare prevention options instead of relying on one deterministic forecast
- I would treat early-stage spread metrics as decision signals, because they help identify whether disruption is likely to accelerate or remain contained

## Start Here

- `PROJECT_SUMMARY.md`: main case-study style overview
- `classroom_flu_simulation.ipynb`: selected simulation workflow
- `utils.py`: simulation engine and plotting helpers

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
