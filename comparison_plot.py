import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. Beräkna teoretiska data (från integral_plot.py, korrigerad) ---

x_values_teori = [0, 2, 4, 6, 8, 10, 12]
z_values_teori = np.linspace(0, 40, 100)  # Använd fler punkter för en jämnare kurva

# Skapa en lista av listor för att lagra punkterna
points = []
for x in x_values_teori:
    row = []
    for z in z_values_teori:
        row.append(np.array([x, 0, z]))
    points.append(row)

points = np.array(points) * 1e-2  # Konvertera till meter

R = 0.155  # Radie (m)
I = 1.018  # Uppmätt ström (A)
N_varv = 150  # Antal varv i spolen

# Numerisk integration
Ntheta = 150  # Antal segment för integrationen
dtheta = 2 * np.pi / Ntheta
theta = dtheta * np.arange(1, Ntheta + 1)

# Beräkna Bz för varje punkt
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

        # Applicera konstanter och antal varv
        # B-fältet från en slinga är (mu0 / 4pi) * integral(...)
        # mu0 / 4pi = 1e-7
        # Konvertera från Tesla till Gauss (1 T = 10^4 G)
        # Multiplicera med antalet varv (N_varv)
        B_final = B * 1e-7 * 1e4 * N_varv
        Bz_row.append(B_final[2])
    Bz_results.append(Bz_row)


# --- 2. Ladda in och förbered experimentella data (från experiment_plot.py) ---


def load_experimental_data(file_path="cleaned_plot_data.csv"):
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Fel: Filen '{file_path}' hittades inte.")
        return None

    # Extrahera serienumret och beräkna x-värdet
    df["series_num"] = df["x_serie"].str.extract(r"(\d+)").astype(int)
    df["x (cm)"] = (df["series_num"] - 1) * 2

    # Konvertera spänning (mV) till magnetfält (Gauss)
    # Kalibreringsfaktor: 4.8 mV/Gauss
    df["Bz (G)"] = df["U_ut (-mV)"] / 4.8

    return df


exp_data = load_experimental_data()


# --- 3. Skapa den kombinerade plotten ---

plt.figure(figsize=(12, 8))

# Hämta standardfärgcykeln från matplotlib
prop_cycle = plt.rcParams["axes.prop_cycle"]
colors = prop_cycle.by_key()["color"]

# Skapa en mappning från x-värde till färg
color_map = {x: colors[i % len(colors)] for i, x in enumerate(x_values_teori)}

# Plotta teoretiska data (linjer)
for i, x in enumerate(x_values_teori):
    plt.plot(
        z_values_teori,
        Bz_results[i],
        linestyle="-",
        label=f"Teori x={x} cm",
        color=color_map[x],
    )

# Plotta experimentella data (punkter) om datan laddades korrekt
if exp_data is not None:
    for x_val in sorted(exp_data["x (cm)"].unique()):
        subset = exp_data[exp_data["x (cm)"] == x_val]
        # Använd samma färg från mappningen, med en fallback ifall x-värdet inte finns
        color = color_map.get(x_val, "k")  # 'k' är svart
        plt.plot(
            subset["z (cm)"],
            subset["Bz (G)"],
            marker="o",
            linestyle="",
            label=f"Mätdata x={x_val:.0f} cm",
            color=color,
        )

# --- 4. Formatera och spara plotten ---

plt.title("Jämförelse av teoretiskt och uppmätt magnetfält $B_z$")
plt.xlabel("$z$ (cm)")
plt.ylabel("$B_z$ (Gauss)")
plt.grid(True, linestyle="--", alpha=0.7)
plt.legend(title="Datatyp och X-position", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout(rect=[0, 0, 0.85, 1])
plt.ylim(0, 14)


# Spara figuren
output_filename = "comparison_plot.png"
plt.savefig(output_filename)
print(f"Plotten har sparats som '{output_filename}'")
plt.show()
plt.close()

# --- 5. Beräkna och plotta delta ---

if exp_data is not None:
    plt.figure(figsize=(12, 8))

    for i, x_val in enumerate(x_values_teori):
        # Hämta teoretiska data för detta x-värde
        bz_teori_for_x = Bz_results[i]

        # Hämta experimentella data för detta x-värde
        subset = exp_data[exp_data["x (cm)"] == x_val]
        if not subset.empty:
            z_exp = subset["z (cm)"]
            bz_exp = subset["Bz (G)"]

            # Interpolera de teoretiska värdena vid de experimentella z-punkterna
            bz_teori_interp = np.interp(z_exp, z_values_teori, bz_teori_for_x)

            # Beräkna skillnaden (delta)
            delta = bz_exp - bz_teori_interp

            # Plotta deltan
            color = color_map.get(x_val, "k")
            plt.plot(
                z_exp,
                delta,
                marker="o",
                linestyle="-",
                label=f"Delta x={x_val} cm",
                color=color,
            )

    plt.title("Skillnad (Delta) mellan uppmätt och teoretiskt $B_z$")
    plt.xlabel("$z$ (cm)")
    plt.ylabel("Delta $B_z$ (Uppmätt - Teoretisk) [Gauss]")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.axhline(
        0, color="black", linewidth=0.8, linestyle="--"
    )  # Noll-linje för referens
    plt.legend(title="X-position", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout(rect=[0, 0, 0.85, 1])

    # Spara figuren
    output_filename_delta = "delta_plot.png"
    plt.savefig(output_filename_delta)
    print(f"Deltaplotten har sparats som '{output_filename_delta}'")
    plt.show()
    plt.close()
