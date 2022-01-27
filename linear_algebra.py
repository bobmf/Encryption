import numpy as np

# set arrays to fun Gausse elimination on

A = np.array([[1.0, 1.0, 1.0], [1.0, -1.0, 0.0], [0.0, 1.0, 2.0]])

B = np.array([5.0, 0.0, 7.0])

# set length of the array
n = len(B)

# set the result vector
x = np.zeros(n)

# forward elimination
for i in range(
    0, n - 1
):  # set first loop to iterate through the two dimensional array = column
    for j in range(i + 1, n):  # second loop responsible for row
        fct = (
            A[j, i] / A[i, i]
        )  # retrive the factor of the number. During the first iteration it will be i=0 and j=1, therefore A[1,0]/A[00] or 1/1
        for k in range(0, n):  # iterate through the whole row j
            A[j, k] -= (
                fct * A[i, k]
            )  # apply the fraction to row i and subtract the result from row j
        B[j] -= fct * B[i]  # repeat on the result vector

# check array A and B
print(A)
print(B)


# backward substitution
x[n - 1] = (
    B[n - 1] / A[n - 1, n - 1]
)  # solve for the last value from the forward elimination
for i in range(n - 2, -1, -1):  # iterate over the array, always skipping the last one
    sum_val = 0  # set the row result to zero
    for j in range(i + 1, n):  # iterate through the number of known variables
        sum_val += A[i, j] * x[j]  # solve and add those variables up
    x[i] = (B[i] - sum_val) / A[
        i, i
    ]  # solve for and add the unkown variables to the results array - starting from n-2

# print out the results
print(x)
