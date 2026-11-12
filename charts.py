
import tkinter as tk
from tkinter import messagebox

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from datetime import datetime


def show_bmi_chart(parent, records, user_name):

    if not records:
        messagebox.showinfo(
            "No BMI History",
            f"No BMI records available for {user_name}."
        )
        return

    try:
        dates = [
            datetime.fromisoformat(record["recorded_at"])
            for record in records
        ]

        bmi_values = [
            float(record["bmi"])
            for record in records
        ]

    except (ValueError, KeyError, TypeError) as error:
        messagebox.showerror(
            "Chart Error",
            f"Could not read BMI history:\n{error}"
        )
        return

    chart_window = tk.Toplevel(parent)
    chart_window.title(f"{user_name} - BMI Trend")
    chart_window.geometry("750x500")
    chart_window.configure(bg="#F4F7F6")

    heading = tk.Label(
        chart_window,
        text=f"{user_name}'s BMI Trend",
        font=("Arial", 18, "bold"),
        bg="#F4F7F6",
        fg="#263238"
    )
    heading.pack(pady=(15, 5))

    figure = Figure(figsize=(8, 4.2), dpi=100)
    axis = figure.add_subplot(111)

    axis.plot(
        dates,
        bmi_values,
        marker="o",
        linewidth=2,
        markersize=7,
        label="BMI"
    )

    axis.axhspan(
        18.5, 24.9,
        alpha=0.10,
        color="green",
        label="Normal range"
    )

    axis.axhline(
        18.5,
        linestyle="--",
        linewidth=1,
        alpha=0.7
    )

    axis.axhline(
        25,
        linestyle="--",
        linewidth=1,
        alpha=0.7
    )

    axis.set_title("BMI Over Time", fontsize=13)
    axis.set_xlabel("Date")
    axis.set_ylabel("BMI")

    axis.xaxis.set_major_formatter(
        mdates.DateFormatter("%d %b %Y")
    )

    figure.autofmt_xdate()
    axis.grid(True, alpha=0.3)
    axis.legend()

    figure.tight_layout()

    canvas = FigureCanvasTkAgg(
        figure,
        master=chart_window
    )

    canvas.draw()
    canvas.get_tk_widget().pack(
        fill="both",
        expand=True,
        padx=15,
        pady=10
    )

    chart_window.protocol(
        "WM_DELETE_WINDOW",
        lambda: close_chart(chart_window, figure)
    )


def close_chart(window, figure):

    plt.close(figure)
    window.destroy()
