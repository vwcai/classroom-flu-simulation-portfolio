import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from scipy.special import comb

class PandemicFluSimulation:
    
    def __init__(self, num_kids=61, days_to_run=126, infection_prob=0.01, recovery_duration=3, n_i_start=1, immune_ratio=0, seed=42):
        """
        Initializes the parameters.
        
        Args:
            num_kids (int): Total number of kids in the classroom (N).
            days_to_run (int): Total number of days the simulation will run (T).
            infection_prob (float): The probability (p) that any single infectious kid
                                    infects any single susceptible kid on a transmission day.
            recovery_duration (int): The number of days a kid is infectious (D).
            n_i_start (int): Initial number of infectious kids at the start of the simulation.
            immune_ratio (float): Proportion of kids who are initially immune (between 0 and 1).

        """

        num_immune_init = int(num_kids * immune_ratio)
        assert num_kids > 0
        assert days_to_run > 0
        assert 0 <= infection_prob <= 1
        assert recovery_duration >= 1

        # Check 1: Initial immune count is non-negative (immune_ratio >= 0)
        assert 0 <= immune_ratio <= 1
    
        # Check 2: Initial infected count is positive
        assert n_i_start >= 1
        
        # Check 3: Initial infected + Initial immune <= Total population
        initial_burden = n_i_start + num_immune_init
        assert initial_burden <= num_kids, (
            f"Initial burden (Infected: {n_i_start} + Immune: {num_immune_init}) "
            f"is {initial_burden}, which exceeds total kids ({num_kids})."
        )

        self.N = num_kids
        self.T = days_to_run
        self.p = infection_prob
        self.D = recovery_duration
        self.immune_ratio = immune_ratio
        self.seed = seed
        self.n_i_start = n_i_start
        
        # State definitions:
        # 0: Susceptible (S_arr)
        # 1, .... D: Infectious (I_arr)
        # D + 1: Recovered (R_arr)

    def _initialize_states(self):
        
        # kid state variable X_arr shape: (N, T + 1), add one extra column at the end for easier state updates
        X_arr = np.zeros((self.N, self.T + 1), dtype=np.int8)
        X_arr[-self.n_i_start:, 0] = 1
        num_immune_init = int((self.N - self.n_i_start)* self.immune_ratio)
        X_arr[:num_immune_init, 0] = self.D + 1  # Set initial immune kids to Recovered state
        
        S_arr = np.zeros(self.T, dtype=np.float64)
        I_arr = np.zeros(self.T, dtype=np.float64)
        R_arr = np.zeros(self.T, dtype=np.float64)
        DeltaI_arr = np.zeros(self.T, dtype=np.float64)
        R_t_arr = np.zeros(self.T, dtype=np.float64)
        np.random.seed(self.seed)

        return X_arr, S_arr, I_arr, R_arr, DeltaI_arr, R_t_arr

    def run_single_simulation(self):
        
        X_arr, S_arr, I_arr, R_arr, DeltaI_arr, R_t_arr = self._initialize_states()
        epidemic_duration = self.T
        time_to_peak = None
        recover_state = self.D + 1
        
        # Iterate through days: t is the index for the current day, t+1 for the next day
        for t in range(self.T):
            
            # Day number starts from 1 (Day 1 = t=0)
            day_number = t + 1
            
            # Check for Weekday (Transmission day). Assuming Day 1 is Monday.
            # (Day number - 1) modulo 7 maps Mon(0) to Sun(6). Weekdays are 0, 1, 2, 3, 4.
            is_weekday = (day_number - 1) % 7 < 5
            
            
            # --- 1. Natural State Progression (Infection Duration and Recovery) ---
            # All states progress one step (X_arr -> X_arr+1) for the next day, t+1
            next_states = X_arr[:, t] + 1
            
            # Maintain terminal states:
            # Recovered kids (State D+1) stay recovered (State D+1)
            next_states[X_arr[:, t] == recover_state] = recover_state
            # Susceptible kids (State 0) temporarily revert to 0 before potential infection
            next_states[X_arr[:, t] == 0] = 0

            # Identify current Infectious Kids (States 1~D)
            infectious_mask = (X_arr[:, t] >= 1) & (X_arr[:, t] <= self.D)
            num_infectious = np.sum(infectious_mask)
            I_arr[t] = num_infectious
            if num_infectious == 0 and epidemic_duration == self.T:
                epidemic_duration = day_number

            # Identify current recovered Kids (State recover state)
            recover_mask = (X_arr[:, t] == recover_state)
            num_recover = np.sum(recover_mask)
            R_arr[t] = num_recover

            # Identify current Susceptible Kids (State 0)

            susceptible_mask = (X_arr[:, t] == 0)
            susceptible_indices = np.where(susceptible_mask)[0]
            num_susceptible = len(susceptible_indices)
            S_arr[t] = num_susceptible


            # --- 2. Transmission Logic (Only applied on Weekdays) ---
            
            if is_weekday:
                
                if num_infectious > 0:
                    # Calculate overall probability of a susceptible kid being infected by at least one source
                    # $P(\text{infection}) = 1 - (1-p)^{\text{num\_infectious}}$
                    prob_of_being_infected = 1.0 - (1.0 - self.p) ** num_infectious
                    

                    R_t_arr[t] = (1.0 - (1.0-self.p) ** self.D) * S_arr[t]
                    
                    if num_susceptible > 0:
                        # Determine who gets newly infected using random rolls
                        random_rolls = np.random.rand(num_susceptible)
                        newly_infected_mask = (random_rolls < prob_of_being_infected) 

                        num_newly_infected = np.sum(newly_infected_mask)
                        DeltaI_arr[t] = num_newly_infected
                        
                        newly_infected_indices = susceptible_indices[newly_infected_mask]
                        
                        # Update the state: Susceptible kids become Day 1 of infection (State 1)
                        next_states[newly_infected_indices] = 1

            # --- 3. Final State Update for Day t+1 ---
            X_arr[:, t + 1] = next_states
        time_to_peak = np.argmax(I_arr) + 1  # Convert to day number
        res = {
            "S": S_arr, 
            "I": I_arr,
            "R": R_arr,
            "DeltaI": DeltaI_arr,
            "R_t": R_t_arr,
            "time_to_peak": time_to_peak,
            "epidemic_duration": epidemic_duration
        }
        return res
    

    def run_monte_carlo(self, num_runs=1000, ci_level=0.95):
        
        T = self.T
        
        # 95% CI Z-score calculation
        alpha = 1.0 - ci_level
        Z_CRITICAL = stats.norm.ppf(1 - alpha / 2) 
        
        # Initialize arrays to collect ALL time series results
        all_S = np.zeros((num_runs, T))
        all_I = np.zeros((num_runs, T))
        all_R = np.zeros((num_runs, T))
        all_DeltaI = np.zeros((num_runs, T))
        all_R_t = np.zeros((num_runs, T))
        
        # Initialize arrays to collect scalar results
        all_time_to_peak = np.zeros(num_runs)
        all_duration = np.zeros(num_runs)
        
        # --- Run Simulations ---
        for i in range(num_runs):
            current_seed = self.seed + i
            # Temporarily override the instance's seed for this run
            temp_seed = self.seed
            self.seed = current_seed
            
            results = self.run_single_simulation()
            self.seed = temp_seed # Restore original seed

            # Collect ALL time series
            all_S[i, :] = results['S']
            all_I[i, :] = results['I']
            all_R[i, :] = results['R'] # <-- New: R
            all_DeltaI[i, :] = results['DeltaI']
            all_R_t[i, :] = results['R_t'] # <-- New: R_t
            
            # Collect scalar metrics
            all_time_to_peak[i] = results['time_to_peak']
            all_duration[i] = results['epidemic_duration']

        # --- Helper function to calculate mean and Z-score CI ---
        def calculate_ci(data, axis=None):
           
            mean = np.mean(data, axis=axis)
            std = np.std(data, axis=axis, ddof=1) # ddof=1 for sample standard deviation
            
            SE = std / np.sqrt(num_runs)
            margin_of_error = Z_CRITICAL * SE
            
            lower_bound = mean - margin_of_error
            upper_bound = mean + margin_of_error
            
            return {
                'mean': mean, 
                '95_lower': lower_bound, 
                '95_upper': upper_bound
            }

        # --- Calculate Statistics for ALL variables ---
        final_results = {
            'S': calculate_ci(all_S, axis=0),
            'I': calculate_ci(all_I, axis=0),
            'R': calculate_ci(all_R, axis=0), # <-- Calculated R
            'DeltaI': calculate_ci(all_DeltaI, axis=0),
            'R_t': calculate_ci(all_R_t, axis=0), # <-- Calculated R_t
            
            # Scalar metrics
            'time_to_peak': calculate_ci(all_time_to_peak),
            'epidemic_duration': calculate_ci(all_duration),
            'all_raw_epidemic_durations': all_duration,
        }
        
        return final_results


def plot_separate_and_mean_combined_results(results, immune_rate=0):
    
    # Check if all required keys are present
    required_keys = ['S', 'I', 'R', 'DeltaI', 'R_t']
    if not all(k in results for k in required_keys):
        print(f"Error: Results must contain keys: {required_keys}")
        return

    T = len(results['S']['mean'])
    days = np.arange(1, T + 1)
    
    # Define plotting information for all 5 variables
    plot_info = [
        {'key': 'S', 'label': 'Susceptible (S)', 'color': 'blue', 'unit': 'Number of Kids'},
        {'key': 'I', 'label': 'Infected (I)', 'color': 'red', 'unit': 'Number of Kids'},
        {'key': 'R', 'label': 'Recovered (R)', 'color': 'green', 'unit': 'Number of Kids'},
        {'key': 'DeltaI', 'label': 'New Cases (DeltaI)', 'color': 'orange', 'unit': 'Number of Cases'},
        {'key': 'R_t', 'label': 'R_t', 'color': 'purple', 'unit': 'R_t Value'},
    ]

    # --- 1. Separate Plots for Mean and CI Bounds (5 Plots) ---
    for info in plot_info:
        data = results[info['key']]
        label = info['label']
        color = info['color']
        unit = info['unit']
        
        plt.figure(figsize=(6, 3))
        
        # Mean (Solid line)
        plt.plot(days, data['mean'], label=f'{label} Mean', color=color, linestyle='-', linewidth=1, marker='o', markersize=2)
        
        # CI Lower Bound (Dotted line)
        plt.plot(days, data['95_lower'], label='95% CI Lower Bound', color=color, linestyle=':', linewidth=1)
        
        # CI Upper Bound (Dotted line)
        plt.plot(days, data['95_upper'], label='95% CI Upper Bound', color=color, linestyle=':', linewidth=1)
        
        plt.fill_between(
            days, 
            data['95_lower'], 
            data['95_upper'], 
            color=color, 
            alpha=0.2,
        )

        plt.title(f'Mean and 95% CI Bounds for {label}, initial immune rate={immune_rate}', fontsize=10)
        plt.xlabel('Day Number', fontsize=10)
        plt.ylabel(unit, fontsize=10)
        plt.gca().tick_params(
            axis='both',
            labelsize=9
        )
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.legend(fontsize=10)
        
        # Special handling for R_t: add the R_t=1 threshold line
        if info['key'] == 'R_t':
            plt.axhline(1.0, color='gray', linestyle='--', linewidth=1, label='R_t=1 Threshold')
            plt.legend(fontsize=10) # Update legend to include the threshold

        plt.tight_layout()
        plt.show()

    # --- 2. Combined Plot for All Mean Trajectories (1 Plot) ---
    
    fig, ax1 = plt.subplots(figsize=(10, 5))
    fig.suptitle(f'Daily Mean of Key Epidemic Variables, initial immurate rate: {immune_rate}', fontsize=10)

    # Create the secondary Y-axis for R_t
    ax2 = ax1.twinx()
    
    # Lists to collect legend handles and labels
    handles = []
    labels = []

    for info in plot_info:
        data = results[info['key']]
        ax = ax1 if info['key'] != 'R_t' else ax2 # Use ax2 only for R_t
        color = info['color']
        label = info['label']
        
        # Plot Mean line
        line, = ax.plot(days, data['mean'], label=f'{label} Mean', color=color, linewidth=1, marker='o', markersize=1.5)

        ax.fill_between(
            days, 
            data['95_lower'], 
            data['95_upper'],  
            color=color,  
            alpha=0.2,
        )
        handles.append(line)
        labels.append(label)

    # R_t = 1 Critical Line (on the right Y-axis)
    R_t_line = ax2.axhline(1.0, color='gray', linestyle='--', linewidth=1, alpha=0.7, label='R_t=1 Threshold')
    handles.append(R_t_line)
    labels.append('R_t=1 Threshold')

    # --- Set Axis Labels and Style ---
    
    # Left Y-axis (S, I, R, DeltaI)
    ax1.set_xlabel('Day Number', fontsize=10)
    ax1.set_ylabel('Number of Kids', color='black', fontsize=10)
    ax1.tick_params(axis='y', labelcolor='black', labelsize=9)
    ax1.tick_params(axis='x', labelcolor='black', labelsize=9)
    ax1.grid(True, linestyle=':', alpha=0.5, which='both')

    # Right Y-axis (R_t)
    ax2.set_ylabel('Effective Reproduction Index (R_t)', color='purple', fontsize=10)
    ax2.tick_params(axis='y', labelcolor='purple', labelsize=9)
    
    # Unified Legend
    fig.legend(handles, labels, loc='center left', bbox_to_anchor=(0.6, 0.5), ncol=1, fontsize=10)
    plt.tight_layout()
    plt.show()


def hist_epidemic_durations(durations, bins=20, immune_rate=0):
    
    plt.figure(figsize=(6, 3))

    plt.hist(
        durations, 
        bins=bins,           
        color='blue',   
        edgecolor='black',  
        alpha=0.5
    )

    plt.title(f'Distribution of Epidemic Duration, initial immune rate={immune_rate}', fontsize=10)
    plt.xlabel('Number of days', fontsize=10)
    plt.ylabel('Frequency', fontsize=10)
    plt.grid(axis='y', alpha=0.5, linestyle=':')
    plt.gca().tick_params(
        axis='both',
        labelsize=9
    )
    plt.tight_layout()
    plt.show()



def count_day2_expected_infections(p=0.01, N=60):
        
    total_sum = 0.0

    for x in range(N + 1):
        # 1. Binomial Probability Mass Function, PMF
        # C(N, x) * p^x * (1-p)^(60-x)
        binom_coeff = comb(N, x)
        
        prob_pmf = binom_coeff * np.power(p, x) * np.power(1 - p, N - x)
        
        # 2. (N - x) * (1 - (1-p)^(x+1))
        # (1-p)^(x+1)
        term_inner_power = np.power(1 - p, x + 1)
        term_summand = (N - x) * (1.0 - term_inner_power) * prob_pmf
        
        # update sum
        total_sum += term_summand
        
    return total_sum