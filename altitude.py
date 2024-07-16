import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Ensure the correct backend is used
plt.switch_backend('TkAgg')

# Function to convert time string to seconds
def time_string_to_seconds(time_str):
    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2])
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

# Read and preprocess data
data = pd.read_csv("pfrcsv.csv")
data["TIME_STAMPING"] = data["TIME_STAMPING"].apply(time_string_to_seconds)
data["TIME_STAMPING"] = data["TIME_STAMPING"] - data["TIME_STAMPING"].min()  # Normalize to start from zero
data = data.rename(columns={'TIME_STAMPING': 'time', 'GNSS_ALTITUDE': 'altitude', 'PRESSURE': 'pressure'})
data_30s = data.head(31)

print("Data loaded and preprocessed.")

# RealTimePlot class definition
class RealTimePlot:
    def __init__(self, root, dataframe):
        print("Initializing RealTimePlot...")
        self.root = root
        self.root.title("Real-Time Plot from DataFrame")

        self.figure, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], 'r-')
        
        # Initial x and y limits
        self.ax.set_xlim(dataframe['time'].min(), dataframe['time'].max())
        self.ax.set_ylim(dataframe['altitude'].min() - 5, dataframe['altitude'].max() + 5)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.data = dataframe
        self.current_index = 0

        self.animation = FuncAnimation(self.figure, self.update_plot, interval=1000, cache_frame_data=False)
        print("RealTimePlot initialized.")

    def update_plot(self, frame):
        print("Updating plot...")
        if self.current_index < len(self.data):
            self.line.set_data(self.data['time'][:self.current_index], self.data['altitude'][:self.current_index])
            self.ax.relim()
            self.ax.autoscale_view()
            self.current_index += 1
            self.canvas.draw()
        print("Plot updated.")

def main():
    print("Starting application...")
    root = tk.Tk()
    app = RealTimePlot(root, data_30s)
    root.mainloop()
    print("Application started.")

if __name__ == "__main__":
    main()
