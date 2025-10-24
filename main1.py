from solver import count_general_constrained_sums
from itertools import product
from typing import List, Set, Dict, Any
import pandas as pd

# --- 1. Define Fixed & Universal Parameters ---
# Groups for exclusion logic
G1 = {1, 4, 7}
G2 = {2, 5, 8}
G3 = {3, 6, 9}

# The universal set from which the pool is generated
UNIVERSAL_SET = {1, 2, 3, 4, 5, 6, 7, 8, 9} 

# Fixed parameters for the system structure:
# Three equations, 2 variables each: x1+x2=b1, x3+x4=b2, x5+x6=b3
SIZES = [2, 2, 2] 
TOTAL_VARIABLES_NEEDED = sum(SIZES) # Requires 6 unique numbers

print("--- Preparing Iterative Combinatorics Test Suite ---")
print(f"System Structure: {len(SIZES)} Equations (Groups of {SIZES})")
print(f"Total Unique Variables Required: {TOTAL_VARIABLES_NEEDED}")
print("-" * 70)

# List to store data for the pandas DataFrame
data_for_df: List[Dict[str, Any]] = []
scenario_count = 0

# --- 2. Generate all 27 scenarios (Pool and Targets) ---
for temp_tuple in product(G1, G2, G3):
    
    # Unpack the elements for calculation
    a, b, c = temp_tuple
    temp_exclusion_set: Set[int] = set(temp_tuple) 
    
    # A. Define the POOL set
    current_pool = list(UNIVERSAL_SET - temp_exclusion_set)
    
    # B. Define the TARGETS list
    sum_temp = a + b + c
    S = (45 + sum_temp) / 3
    
    T1 = S - (a + b)
    T2 = S - (a + c)
    T3 = S - (c + b)
    
    # Check if S is an integer (ensuring targets are integers)
    if S != int(S):
        print(f"[ERROR] S is not an integer for {temp_tuple}. Skipping scenario.")
        continue
        
    current_targets = [int(T1), int(T2), int(T3)]
    
    # --- Execute and Store ---
    
    # Check if the resulting pool is large enough
    if len(current_pool) < TOTAL_VARIABLES_NEEDED:
        print(f"[ERROR] Skipping scenario {temp_tuple}: Pool size ({len(current_pool)}) too small.")
        continue

    # Run the generalized function
    solution_count = count_general_constrained_sums(current_targets, SIZES, current_pool)
    
    # 3. Store the results in the list of dictionaries
    data_for_df.append({
        '(a,b,c)': temp_tuple,
        'Targets (b1,b2,b3)': tuple(current_targets),
        'Solutions Found': solution_count,
        'S': S,
    })
    scenario_count += 1


# --- 4. Generate and Print the Final Table ---
if data_for_df:
    df = pd.DataFrame(data_for_df)
    
    # Set the index (row number) starting from 1 for better readability
    df.index = pd.RangeIndex(start=1, stop=len(df) + 1) 

    print("\n\n" + "=" * 70)
    print(f"RESULTS SUMMARY: {scenario_count} Unique Test Cases")
    print("=" * 70)
    
    # Use to_string() to ensure the entire table is printed clearly in the console
    print(df.to_string())
    print("=" * 70)
else:
    print("No scenarios were run due to validation failures.")
