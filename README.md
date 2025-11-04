# Labb 4: Magnetfält från en spole

Detta projekt analyserar och visualiserar magnetfältet från en strömförande spole. Det jämför experimentellt uppmätta värden med teoretiska beräkningar baserade på Biot-Savarts lag.

## Filer och skript

-   `plotdata.csv`: Rådata från mätningarna.
-   `cleaned_plot_data.csv`: Städad och formaterad data som används av skripten.
-   `experiment_plot.py`: Läser in den städade datan, konverterar mätvärden (mV) till magnetfält (Gauss) och plottar det uppmätta magnetfältet ($B_z$) som en funktion av positionen ($z$) för olika tvärgående positioner ($x$). Resultatet sparas som `experiment_plot.png`.
-   `integral_plot.py`: Beräknar det teoretiska magnetfältet ($B_z$) genom numerisk integration av Biot-Savarts lag för en spole med samma geometri och ström som i experimentet. Resultatet sparas som `integral_plot.png`.
-   `comparison_plot.py`: Jämför de experimentella och teoretiska resultaten i en och samma graf. Plottar även skillnaden (delta) mellan mätdata och teori. Resultaten sparas som `comparison_plot.png` och `delta_plot.png`.

## Resultat

Projektet genererar följande visualiseringar:

-   `experiment_plot.png`: Visar det uppmätta magnetfältet.
-   `integral_plot.png`: Visar det teoretiskt beräknade magnetfältet.
-   `comparison_plot.png`: Jämför de uppmätta och teoretiska värdena.
-   `delta_plot.png`: Visar den procentuella skillnaden mellan teori och experiment.

## Hur man kör

För att återskapa resultaten, kör följande skript (uv):

1.  `uv run experiment_plot.py`
2.  `uv run integral_plot.py`
3.  `uv run comparison_plot.py`

För att återskapa resultaten, kör följande skript (python):

1.  `python experiment_plot.py`
2.  `python integral_plot.py`
3.  `python comparison_plot.py`

Detta kommer att generera alla `.png`-filer baserat på den inkluderade `cleaned_plot_data.csv`-filen.
