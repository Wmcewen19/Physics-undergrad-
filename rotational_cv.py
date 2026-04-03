import numpy as np
import matplotlib.pyplot as plt

# --- STEP 1: CREATE THE UNIVERSE ---
# I'm setting my fundamental constants to 1.0 because I only care about 
# the RATIO of energy to temperature. This makes my math universal!
k = 1.0
epsilon = 1.0

# I need a range of 'Dimensionless Temperatures' (kT/epsilon) from near-zero to 3.
# I'll use 500 points to make the curves as smooth as possible.
temp_ratio = np.linspace(0.01, 3.0, 500) 

# The problem demands I stop at J=6. Let's see if the universe agrees.
J_max = 6  

def simulate_rotational_physics(T_list, j_limit):
    cv_results = []
    
    for tr in T_list:
        # Since my x-axis is kT/epsilon, and my Boltzmann exponent is epsilon/kT,
        # I must invert the temperature to get my scaling factor.
        beta_eps = 1.0 / tr
        
        # --- STEP 2: SUMMON THE QUANTUM STATES ---
        # I'm creating a vector of J values from 0 to 6.
        j = np.arange(j_limit + 1)
        
        # Energy levels: E = epsilon * J * (J + 1)
        energies = epsilon * j * (j + 1)
        
        # Degeneracy: Nature says there are (2J + 1) ways to be in each state!
        degeneracies = 2 * j + 1
        
        # --- STEP 3: THE BOLTZMANN WEIGHTS ---
        # Each state's importance is weighed by its degeneracy and its energy.
        # This is the 'State Counter' logic.
        weights = degeneracies * np.exp(-j * (j + 1) * beta_eps)
        
        # --- STEP 4: EXTRACT THERMODYNAMICS ---
        # The Partition Function Z is just the sum of these weights.
        Z = np.sum(weights)
        
        # Average Energy <E> is the energy-weighted sum divided by the total tally.
        E_avg = np.sum(energies * weights) / Z
        
        # I need <E^2> to calculate the fluctuations (heat capacity).
        E2_avg = np.sum((energies**2) * weights) / Z
        
        # Heat Capacity formula using the Variance of Energy:
        # Cv = (<E^2> - <E>^2) / (k * T^2). 
        # This is the most efficient way to avoid messy numerical derivatives!
        cv = (E2_avg - E_avg**2) / (k * tr**2)
        cv_results.append(cv)
        
    return np.array(cv_results)

# --- STEP 5: RUN THE EXPERIMENT ---
cv_vals = simulate_rotational_physics(temp_ratio, J_max)

# --- STEP 6: VISUAL PROOF ---
plt.figure(figsize=(10, 6))
plt.plot(temp_ratio, cv_vals, color='cyan', lw=2.5, label=f'Exact Sum (J=0 to {J_max})')

# The Classical Limit is my 'ceiling'. It represents the 2 degrees of freedom (Nk).
plt.axhline(y=1.0, color='red', linestyle='--', label='Classical Limit (NK)')

plt.title("Rotational Heat Capacity: The J=6 Limit", fontsize=14)
plt.xlabel(r"Dimensionless Temperature ($kT/\epsilon$)", fontsize=12)
plt.ylabel(r"Heat Capacity ($C_V / Nk$)", fontsize=12)
plt.grid(alpha=0.2, color='white') # High contrast for the dark lab vibe
plt.gca().set_facecolor('#121212') # Dark mode for maximum vibes
plt.ylim(0, 1.5)
plt.legend()
plt.show()

