import numpy as np

# Define the data points in a more structured way
x_values = [0, 2, 4, 6, 8, 10, 12]
z_values = [0, 5, 10, 15, 20, 25, 30, 35, 40]

# Create a list of lists to store the points
points = []
for x in x_values:
    row = []
    for z in z_values:
        row.append(np.array([x, 0, z]))
    points.append(row)

points = np.array(points) * 1e-2  # convert to meters

R = 0.155  # Radius (m)
I = 1  # Current (A)
mu_0 = 4 * np.pi * 1e-7
Ntheta = 150  # Number of segments
dtheta = 2 * np.pi / Ntheta
theta = dtheta * np.arange(1, Ntheta + 1)

# Calculate Bz for each point
Bz_results = []
for row in points:
    Bz_row = []
    for p in row:
        B = np.array([0.0, 0.0, 0.0])
        for k in np.arange(Ntheta):
            r = np.array(
                [
                    p[0] - R * np.cos(theta[k]),
                    p[1] - R * np.sin(theta[k]),
                    p[2],
                ]
            )
            ds = dtheta * np.array([-R * np.sin(theta[k]), R * np.cos(theta[k]), 0])
            dB = I * np.cross(ds, r) / np.linalg.norm(r) ** 3
            B = B + dB
        B = B * 1e-7 * 1e4  # with μ0/4π (G)
        Bz_row.append(B[2] * Ntheta)  # Calculate the result for N thtreads
    Bz_results.append(Bz_row)

# z-värden i meter
z_array_m = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40]) * 1e-2

# Beräkna exakta Bz i Tesla
Bz_exakt_T = (mu_0 * (Ntheta * I) * R**2) / (2 * (R**2 + z_array_m**2) ** (1.5))

# Omvandla till Gauss
Bz_exakt_Gauss = Bz_exakt_T * 1e4

# döp om array för läsbarhet
Bz_numerisk = np.array(Bz_results[0])

# Beräkna det absoluta felet
absolut_fel = np.abs(Bz_numerisk - Bz_exakt_Gauss)

print("Största absoluta fel (Gauss):", np.max(absolut_fel))
