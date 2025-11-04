import numpy as np
import matplotlib.pyplot as plt

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


plt.figure(figsize=(10, 6))
for i, x in enumerate(x_values):
    plt.plot(z_values, Bz_results[i], marker=None, linestyle="-", label=f"x = {x} cm")

plt.title("$Bz$ som funktion av $z$ för olika $x$-positioner (beräknade värden)")
plt.xlabel("$z$ (cm)")
plt.ylabel("$Bz$ (G)")
plt.ylim(0, 14)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(title="X-position", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout(rect=[0, 0, 0.85, 1])  # Justera för att få plats med legend

# Spara figuren
output_filename = "integral_plot.png"
plt.savefig(output_filename)
plt.show()
plt.close()
