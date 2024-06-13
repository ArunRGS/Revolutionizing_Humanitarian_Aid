import tkinter as tk
from tkinter import messagebox
import requests
import time
import math
import folium

class DroneSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Drone Simulator")

        self.create_input_fields()
        self.create_buttons()

        self.status_label = tk.Label(root, text="")
        self.status_label.pack()

        self.speed_label = tk.Label(root, text="")
        self.speed_label.pack()

        self.location_label = tk.Label(root, text="")
        self.location_label.pack()

        self.time_label = tk.Label(root, text="")
        self.time_label.pack()

        self.wind_speed_label = tk.Label(root, text="")
        self.wind_speed_label.pack()

        # Initialize Folium map
        self.map = folium.Map(location=[0, 0], zoom_start=2)
        self.map_marker = folium.Marker(location=[0, 0], popup='Drone').add_to(self.map)
        self.map_frame = tk.Frame(self.root)
        self.map_frame.pack()
        self.map_label = tk.Label(self.map_frame)
        self.map_label.pack()

    def create_input_fields(self):
        self.from_label = tk.Label(self.root, text="From (city):")
        self.from_label.pack()
        self.from_entry = tk.Entry(self.root)
        self.from_entry.pack()

        self.to_label = tk.Label(self.root, text="To (city):")
        self.to_label.pack()
        self.to_entry = tk.Entry(self.root)
        self.to_entry.pack()

    def create_buttons(self):
        self.fly_button = tk.Button(self.root, text="Fly Drone", command=self.fly_drone)
        self.fly_button.pack()

    def fly_drone(self):
        from_city = self.from_entry.get().strip()
        to_city = self.to_entry.get().strip()

        if not from_city or not to_city:
            messagebox.showerror("Error", "Please enter both 'from' and 'to' cities.")
            return

        # Call API to get coordinates for 'from' and 'to' cities
        from_coords = self.get_coordinates(from_city)
        to_coords = self.get_coordinates(to_city)

        if from_coords and to_coords:
            # Calculate flight path (simplified for demonstration)
            flight_path = [from_coords, to_coords]

            total_distance = self.calculate_distance(from_coords, to_coords)
            fake_wind_speed = 2  # Fake wind speed in m/s

            # Simulate flight along the flight path
            for i in range(len(flight_path)):
                current_location = flight_path[i]
                self.status_label.config(text=f"Drone is flying to {to_city}")
                self.location_label.config(text=f"Current Location: {current_location}")
                self.root.update()

                # Update Folium map with current location
                self.update_map(current_location)

                # Calculate estimated time of arrival
                estimated_time = self.calculate_time(total_distance, fake_wind_speed)
                self.time_label.config(text=f"Estimated Time of Arrival: {estimated_time} seconds")

                # Simulate delay between waypoints
                self.simulate_delay(5)  # Simulate 5 seconds delay

                # Fetch real-time weather data for the current location
                weather_data = self.get_weather_data(current_location)
                if weather_data:
                    self.speed_label.config(text=f"Current Speed: {weather_data['wind']['speed']} m/s")
                    self.wind_speed_label.config(text=f"Wind Speed: {fake_wind_speed} m/s")

            messagebox.showinfo("Success", "Drone has reached the destination.")

    def get_coordinates(self, city):
        api_key = '980c1856e3cb44db9049f54b9c565321'  # Replace with your actual API key

        params = {
            "q": city,
            "key": api_key,
            "no_annotations": 1
        }

        try:
            response = requests.get("https://api.opencagedata.com/geocode/v1/json", params=params)
            data = response.json()

            if data["status"]["code"] == 200:
                # Extract latitude and longitude from the response
                latitude = data["results"][0]["geometry"]["lat"]
                longitude = data["results"][0]["geometry"]["lng"]
                return latitude, longitude
            else:
                messagebox.showerror("Error", f"Failed to retrieve coordinates: {data['status']['message']}")
                return None

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return None

    def calculate_distance(self, from_coords, to_coords):
        # Calculate distance between two coordinates (simplified using Euclidean distance)
        return math.sqrt((to_coords[0] - from_coords[0]) ** 2 + (to_coords[1] - from_coords[1]) ** 2)

    def calculate_time(self, distance, speed):
        # Calculate estimated time of arrival (time = distance / speed)
        return distance / speed if speed != 0 else float('inf')

    def simulate_delay(self, seconds):
        # Simulate delay (in seconds)
        time.sleep(seconds)

    def get_weather_data(self, location):
        api_key = '46ea7ed7f8c3332c747025adaac44720'  # Replace with your OpenWeatherMap API key

        params = {
            "lat": location[0],
            "lon": location[1],
            "appid": api_key
        }

        try:
            response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)
            data = response.json()

            if response.status_code == 200:
                return data
            else:
                messagebox.showerror("Error", f"Failed to retrieve weather data: {data.get('message', 'Unknown error')}")
                return None

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching weather data: {str(e)}")
            return None

    def update_map(self, location):
        # Update Folium map marker with new location
        self.map_marker.location = location
        self.map_label.config(text="")
        self.map_label.pack_forget()
        self.map_label.pack()
        self.map_label.update()
        # Clear previous map
        self.map_label.pack_forget()
        self.map_label.pack()
        # Display updated map
        self.map_label.pack_forget()
        self.map_label.pack()
        self.map_label.update()

def main():
    root = tk.Tk()
    app = DroneSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
