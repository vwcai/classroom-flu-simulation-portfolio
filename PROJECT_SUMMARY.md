# Project Summary

## Executive Summary

This project uses Monte Carlo simulation to evaluate how pre-existing immunity changes flu spread in a classroom setting. Two scenarios were tested over 5,000 simulation runs: one with no initial immunity and one with 50% initial immunity.

The main result is clear: higher initial immunity materially reduces both outbreak size and outbreak duration. In the simulated classroom, raising initial immunity from 0% to 50% lowers expected total infections from about 12.10 students to about 2.90 students and cuts expected epidemic duration from about 11.91 days to about 6.45 days.

From a business analytics perspective, the project illustrates how scenario modeling can quantify the operational value of preventive action before a disruption spreads. It also shows how a simple simulation can turn assumptions into measurable decision metrics.

## Business Question

How much can an upfront preventive condition reduce downstream disruption?

In this case, the preventive condition is initial immunity and the disruption is the spread of flu through a classroom. The same analytical framing can apply to business settings such as staffing risk, supply chain disruption, customer churn contagion, or operational incident spread.

## Analytical Approach

- Built a stochastic discrete-time individual-based SIR simulation in Python
- Modeled a closed, high-contact classroom population of 61 students
- Tracked susceptible, infected, and recovered students over time
- Modeled weekday-only transmission and fixed recovery duration
- Ran 5,000 Monte Carlo iterations for each scenario
- Compared expected infection trajectories, time to peak, and epidemic duration across scenarios
- Exported summary outputs for review and visualization

## Model Framing

The simulation adapts the classical SIR framework to a discrete-time, individual-level setting. Each student is represented explicitly and can move through susceptible, infected, and recovered states over time.

This framing is useful because it keeps the model intuitive while still allowing uncertainty, repeated simulation, and scenario comparison. It also makes the project easier to explain to non-technical stakeholders than a purely equation-driven epidemiology model.

## Scenario Design

| Scenario | Initial Immunity | Students | Days Simulated | Infection Probability | Recovery Duration |
| --- | ---: | ---: | ---: | ---: | ---: |
| Simulation 1 | 0% | 61 | 63 | 0.01 | 3 days |
| Simulation 2 | 50% | 61 | 63 | 0.01 | 3 days |

## Validation Check

The report also includes a simple analytical benchmark for early-stage spread:

- On Day 1, the number of new infections follows a binomial distribution with expected value **0.6**
- By Day 2, the analytically derived expected cumulative infections are approximately **2.53995**
- The simulation estimate is **2.5447**, which is very close to the analytical result

This comparison helps validate that the simulation logic is behaving as intended.

## Key Findings

| Metric | 0% Immunity | 50% Immunity |
| --- | ---: | ---: |
| Mean time to peak | 5.41 days | 2.46 days |
| Mean epidemic duration | 11.91 days | 6.45 days |
| Expected infections by Day 1 | 1.6036 | 1.3002 |
| Expected infections by Day 2 | 2.5446 | 1.6820 |
| Final expected accumulated infections | 12.1022 | 2.9040 |

Viewed as a share of the classroom, the final expected outbreak size falls from roughly **20%** of students to roughly **5%** when initial immunity rises from 0% to 50%.

Another important directional result is the effective reproduction pattern:

- With **0% initial immunity**, transmission remains self-sustaining early on and `Rt` drops below 1 only later in the outbreak
- With **50% initial immunity**, `Rt` stays below 1 from the beginning, so the outbreak is quickly suppressed

## Business Interpretation

The results show the value of prevention in measurable operational terms:

- Higher initial protection leads to fewer total disruptions
- The disruption period ends sooner, reducing the window of exposure
- Early-stage spread slows, which gives decision-makers more time to respond
- Small changes in initial conditions can create large downstream differences

This is the kind of problem business analytics often addresses: compare scenarios, quantify risk reduction, and translate results into practical decision support.

## Why This Matters

While this project uses an epidemic setting, the analytical pattern is broadly transferable. The same workflow can support questions such as:

- How much does preventive investment reduce expected losses?
- How does early intervention change the duration of a disruption?
- Which scenarios create the largest difference in downstream outcomes?

The project can also be framed as a small-scale operations risk problem for environments such as classrooms, daycare centers, or office teams where close contact can amplify disruption.

The project demonstrates both technical implementation and the ability to frame modeling results in a decision-oriented way.

## Limitations

- The model uses simplified assumptions, including a fixed infection probability and recovery duration
- Transmission is limited to weekdays only
- The simulation does not incorporate heterogeneous behavior, network structure, or varying susceptibility
- Results should be interpreted as scenario-based estimates rather than real-world forecasts

## Files

- `classroom_flu_simulation.ipynb`: notebook with simulation workflow and visual outputs
- `utils.py`: simulation and plotting utilities
- `sim_1_expected_num_of_accumulated_infections.csv`: exported scenario 1 results
- `sim_2_expected_num_of_accumulated_infections.csv`: exported scenario 2 results
