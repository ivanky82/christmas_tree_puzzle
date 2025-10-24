from itertools import permutations

def count_general_constrained_sums(target_sums: list[int], group_sizes: list[int], pool: list[int]) -> int:
    """
    Finds the number of unique solutions for a general system of equations 
    where all variables must be unique and taken from the pool.
    
    The system is defined by:
    x1 + ... + x_n1 = b1
    x_{n1+1} + ... + x_{n1+n2} = b2
    ... etc.

    IMPORTANT NOTE: This version implements the logic 
    that the order of variables *within* each group (equation) 
    does not matter (combinations).
    E.g., for x1+x2=7, (1, 6) and (6, 1) are counted as a single solution 
    set {1, 6}. 
    The order of the *groups* themselves (the equations) still matters.

    Inputs:
        target_sums: List of target values [b1, b2, b3, ...].
        group_sizes: List where each element is the number of variables 
                     in the corresponding equation [n1, n2, n3, ...].
        pool: The list of available unique numbers (e.g., [1, 2, 3, 4, 5, 6]).
        
    Returns:
        The total number of valid solution sets (partitions).
    """
    
    # 1. Calculate the total number of variables (N) needed
    N = sum(group_sizes)
    
    # Use a set to store canonical forms of solutions. A canonical form 
    # ignores the internal order of elements within each group.
    unique_solution_sets = set()
    
    # Validation: Check if the pool is large enough
    if len(pool) < N:
        print(f"Error: Pool size ({len(pool)}) is too small. Need {N} unique numbers.")
        return 0 
        
    # 2. Generate all unique arrangements (permutations) of N numbers 
    # chosen from the pool.
    # We still need permutations here to ensure we check every unique 
    # assignment of numbers to the groups (equations).
    all_unique_arrangements = permutations(pool, N)
    
    for p in all_unique_arrangements:
        
        current_index = 0
        all_equations_match = True
        canonical_grouping = []
        
        # 3. Check constraints by slicing the permutation into groups
        for target, size in zip(target_sums, group_sizes):
            # Extract the variables for the current equation
            group = p[current_index : current_index + size]
            
            # Check if the sum matches the target
            if sum(group) != target:
                all_equations_match = False
                break # Exit loop if this equation fails
            
            # Create a canonical representation: sort the numbers within the group.
            # This ensures that (1, 6) and (6, 1) both result in the key (1, 6).
            canonical_group = tuple(sorted(group))
            canonical_grouping.append(canonical_group)
            
            # Move the starting point for the next equation
            current_index += size

        # 4. If all equations matched, add the canonical grouping to the set.
        # The key is a tuple of sorted tuples, guaranteeing that only the 
        # choice of numbers for each ordered equation is counted once.
        if all_equations_match:
            unique_solution_sets.add(tuple(canonical_grouping))
            
    # 5. The final count is the size of the set of unique solution partitions.
    return len(unique_solution_sets)
