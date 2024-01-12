import torch
import torch.nn.functional as F

# Your tensor
input_tensor = torch.tensor([[1.1901e+09, 9.6131e+08, 2.1982e+09, 2.6441e+08, 7.3759e+08, 0.0000e+00,
                             0.0000e+00, 0.0000e+00, 8.5875e+08, 2.4604e+09]])

# Apply softmax along the second dimension
output_tensor = F.softmax(input_tensor, dim=1)

# Convert the tensor to a NumPy array (as a probability distribution)
prob_distribution = output_tensor.detach().numpy()

# Print the input tensor, softmax output tensor, and probability distribution
print("Input Tensor:")
print(input_tensor)

print("\nSoftmax Output Tensor:")
print(output_tensor)

print("\nProbability Distribution (as NumPy array):")
print(prob_distribution)
