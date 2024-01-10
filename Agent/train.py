import numpy as np

# Assuming you have an array named 'arr'
arr = np.array([0, 3, 0, 7, 0, 9, 2, 0, 6, 0])

# Get a boolean mask for non-zero elements in the first 5 elements
nonzero_mask = arr[:5] != 0

# Get the indices of non-zero elements
nonzero_indices = np.where(nonzero_mask)[0][0]

# Print the result
print("Array:", arr)
print("Non-zero elements in the first 5 elements:", arr[:5][nonzero_mask])
print("Indices of non-zero elements:", nonzero_indices)
