import pandas as pd
import matplotlib.pyplot as plt


def plot_cleaned_data(file_path="cleaned_plot_data.csv"):
    """
    Läser in den städade CSV-filen och plottar U_ut mot z för varje x-serie,
    med korrekta x-värden (0, 2, 4, ..., 12) som etiketter.
    """

    # --- 1. Ladda in data ---
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(
            f"Fel: Filen '{file_path}' kunde inte hittas. Se till att filen är uppladdad."
        )
        return
    except Exception as e:
        print(f"Ett fel uppstod vid inläsning av filen: {e}")
        return

    # --- 2. Beräkna de korrekta x-värdena ---

    # Extrahera serienumret från strängen 'Serie N'
    df["series_num"] = df["x_serie"].str.extract(r"(\d+)").astype(int)

    # Beräkna x-värdet baserat på regeln: x = (serienummer - 1) * 2
    df["x (cm)"] = (df["series_num"] - 1) * 2

    # konvertera till Gauss (n Gauss =  U_ut(mV) / 4.8 mV )
    df["U_ut (-mV)"] = df["U_ut (-mV)"] / 4.8

    # --- 3. Skapa plotten ---

    plt.figure(figsize=(10, 6))

    # Plotta varje serie individuellt
    for x_val in sorted(df["x (cm)"].unique()):
        subset = df[df["x (cm)"] == x_val]
        plt.plot(
            subset["z (cm)"],
            subset["U_ut (-mV)"],
            marker="o",
            linestyle="",
            label=f"x = {x_val:.0f} cm",
        )

    # --- 4. Formatera och spara plotten ---

    plt.title("$Bz$ som funktion av $z$ för olika $x$-positioner (uppmätta data)")
    plt.xlabel("$z$ (cm)")
    plt.ylabel("$Bz$ (G)")
    plt.ylim(0, 14)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(title="X-position", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout(rect=[0, 0, 0.85, 1])  # Justera för att få plats med legend

    # Spara figuren
    output_filename = "experiment_plot.png"
    plt.savefig(output_filename)
    plt.show()
    plt.close()


# Kör funktionen
plot_cleaned_data()
