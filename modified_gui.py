import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
data["TIME_STAMPING"] = data["TIME_STAMPING"] - 69
data['time_diff'] = data['TIME_STAMPING'].diff()
data['altitude_diff'] = data['ALTITUDE'].diff()

# Compute the velocity (rate of change of altitude)
data['velocity'] = data.apply(lambda row: row['altitude_diff'] / row['time_diff'] if row['time_diff'] != 0 else None, axis=1)

data = data.rename(columns={'TIME_STAMPING': 'time', 'GNSS_ALTITUDE': 'altitude', 'PRESSURE': 'pressure'})
data_30s = data.head(31)

# RealTimePlot class definition
class RealTimePlot:
    def __init__(self, root, dataframe):
        self.root = root
        self.root.title("Real-Time Plot from DataFrame")
        
        # Create a frame for the plot and the controls
        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Create and pack the plot canvas
        self.figure, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], 'r-')
        
        self.plot_type = None  # Initially no plot type selected
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Dropdown menu for selecting plot type
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(side=tk.TOP, fill=tk.X)

        self.label = tk.Label(self.input_frame, text="Select plot type:")
        self.label.pack(side=tk.LEFT)

        self.plot_type_var = tk.StringVar()
        self.plot_type_var.set('')  # Initially no selection
        self.plot_type_dropdown = ttk.Combobox(self.input_frame, textvariable=self.plot_type_var, values=['velocity', 'pressure', 'altitude'])
        self.plot_type_dropdown.pack(side=tk.LEFT)

        self.button = tk.Button(self.input_frame, text="Plot", command=self.update_plot_type)
        self.button.pack(side=tk.LEFT)

        self.data = dataframe
        self.current_index = 0

        self.animation = FuncAnimation(self.figure, self.update_plot, interval=1000, cache_frame_data=False)

    def update_plot(self, frame):
        if self.plot_type and self.current_index < len(self.data):
            self.line.set_data(self.data['time'][:self.current_index], self.data[self.plot_type][:self.current_index])
            self.ax.relim()
            self.ax.autoscale_view()
            self.current_index += 1
            self.canvas.draw()

    def update_plot_type(self):
        plot_type = self.plot_type_var.get().strip().lower()
        if plot_type in ['velocity', 'pressure', 'altitude']:
            self.plot_type = plot_type
            self.update_y_limits(self.data)  
            self.current_index = 0  
        else:
            tk.messagebox.showerror("Invalid Input sir")
            self.plot_type = None  

    def update_y_limits(self, dataframe):
        if self.plot_type:
            self.ax.set_ylim(dataframe[self.plot_type].min() - 5, dataframe[self.plot_type].max() + 5)

def main():
    root = tk.Tk()
    app = RealTimePlot(root, data_30s)
    root.mainloop()

if __name__ == "__main__":
    main()
