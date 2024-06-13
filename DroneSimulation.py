import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class DroneSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Drone Simulator")

        self.canvas_width = 500
        self.canvas_height = 500
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        self.label = tk.Label(root, text="Enter coordinates:")
        self.label.pack()

        # Latitude entry
        self.lat_label = tk.Label(root, text="Latitude:")
        self.lat_label.pack()
        self.lat_entry = tk.Entry(root)
        self.lat_entry.pack()

        # Longitude entry
        self.long_label = tk.Label(root, text="Longitude:")
        self.long_label.pack()
        self.long_entry = tk.Entry(root)
        self.long_entry.pack()

        # Speed slider
        self.speed_label = tk.Label(root, text="Speed:")
        self.speed_label.pack()
        self.speed_slider = ttk.Scale(root, from_=1, to=10, orient="horizontal")
        self.speed_slider.pack()

        # Drone color selection
        self.color_label = tk.Label(root, text="Drone Color:")
        self.color_label.pack()
        self.color_entry = tk.Entry(root)
        self.color_entry.insert(tk.END, "red")  # Default color
        self.color_entry.pack()

        # Fly button
        self.button = tk.Button(root, text="Fly Drone", command=self.fly_drone)
        self.button.pack()

        # Clear button
        self.clear_button = tk.Button(root, text="Clear", command=self.clear_drone)
        self.clear_button.pack()

        self.status_label = tk.Label(root, text="")
        self.status_label.pack()

        # Drone representation
        self.drone = None
        self.arrow = None

    def fly_drone(self):
        if self.arrow:
            messagebox.showerror("Error", "Drone is already flying.")
            return

        # Get input coordinates
        latitude = self.lat_entry.get().strip()
        longitude = self.long_entry.get().strip()

        # Validate input coordinates
        if not latitude or not longitude:
            messagebox.showerror("Error", "Please enter both latitude and longitude.")
            return

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numeric values for latitude and longitude.")
            return

        if not (0 <= latitude <= self.canvas_width and 0 <= longitude <= self.canvas_height):
            messagebox.showerror("Error", "Coordinates are out of bounds.")
            return

        speed = self.speed_slider.get()
        color = self.color_entry.get()

        self.status_label.config(text=f"Drone is flying to coordinates: ({latitude}, {longitude})")
        self.root.update()

        # Simulate drone movement
        self.move_drone(latitude, longitude, speed, color)

    def move_drone(self, latitude, longitude, speed, color):
        # Calculate movement steps based on speed
        steps = 100
        dx = (latitude - self.canvas_width / 2) / steps
        dy = (longitude - self.canvas_height / 2) / steps

        # Move the drone towards the destination
        self.move_drone_step(dx, dy, steps, speed, color)

    def move_drone_step(self, dx, dy, steps, speed, color):
        x, y = self.canvas_width / 2, self.canvas_height / 2
        print(f"Initial x, y: {x}, {y}")

        if steps > 0:
            if self.arrow:
                self.canvas.move(self.arrow, dx * speed, dy * speed)
            else:
                x2 = x + dx * speed
                y2 = y + dy * speed
                print(f"Final x, y: {x2}, {y2}")

                if 0 <= x2 <= self.canvas_width and 0 <= y2 <= self.canvas_height:
                    self.arrow = self.canvas.create_line(x, y, x2, y2, arrow=tk.LAST, fill=color)
                else:
                    print("Destination out of bounds.")
            self.root.after(50, self.move_drone_step, dx, dy, steps - 1, speed, color)
            self.status_label.config(text=f"Drone is at coordinates: ({x}, {y})")
        else:
            self.status_label.config(text="Drone has reached the destination.")
            messagebox.showinfo("Success", "Drone has reached the destination.")

    def clear_drone(self):
        if self.arrow:
            self.canvas.delete(self.arrow)
            self.arrow = None
            self.status_label.config(text="Drone cleared.")
        else:
            messagebox.showerror("Error", "No drone to clear.")

def main():
    root = tk.Tk()
    app = DroneSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
