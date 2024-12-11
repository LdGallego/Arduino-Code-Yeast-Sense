import customtkinter as ctk
from PIL import Image
import serial
from datetime import datetime
from collections import deque

# Initialize the serial port
ser = serial.Serial('COM3', 9600)

# Main application
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Yeast Monitoring System")
        self.geometry("300x400")  # Adjusted height to fit the content
        self.grid_columnconfigure(0, weight=1)

        # Adjust row weights to allow flexible resizing
        self.grid_rowconfigure(2, weight=1)  

        # Data storage for the labels
        self.timestamps = deque(maxlen=12)  # Store timestamps for 1 hour (5 min intervals)
        self.temperatures = deque(maxlen=12)  # Store temperatures
        self.ph_values = deque(maxlen=12)  # Store pH values

        # Setup main page
        self.setup_main_page()

        # Start updating the labels with serial data
        self.update_serial_labels()

    def setup_main_page(self):
        # Title
        title_label = ctk.CTkLabel(self, text="Yeast Monitoring System", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 20), sticky="ew")

        # Image
        image = Image.open("YeastImg.jpeg")
        self.image_ctk = ctk.CTkImage(light_image=image, size=(500, 400))  # Adjust size if needed
        image_label = ctk.CTkLabel(self, image=self.image_ctk, text="")
        image_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Frame for readings
        readings_frame = ctk.CTkFrame(self)
        readings_frame.grid(row=2, column=0, padx=10, pady=(10, 30), sticky="nsew")
        readings_frame.grid_columnconfigure(0, weight=1)

        # Frame Title
        frame_title = ctk.CTkLabel(readings_frame, text="Readings", font=("Arial", 14, "bold"))
        frame_title.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")

        # Temperature Section
        temp_title_label = ctk.CTkLabel(readings_frame, text="Temperature:", font=("Arial", 12))
        temp_title_label.grid(row=1, column=0, padx=10, pady=(10, 2), sticky="w")

        self.temp_label = ctk.CTkLabel(readings_frame, text="-- °C", font=("Arial", 12))
        self.temp_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        # pH Section
        ph_title_label = ctk.CTkLabel(readings_frame, text="pH:", font=("Arial", 12))
        ph_title_label.grid(row=3, column=0, padx=10, pady=(10, 2), sticky="w")

        self.ph_label = ctk.CTkLabel(readings_frame, text="--", font=("Arial", 12))
        self.ph_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

    def update_serial_labels(self):
        # Read and update serial data
        def read_serial():
            if ser.in_waiting > 0:
                lines = ser.read_until().decode('utf-8').strip().split("\n")

                # Initialize placeholders
                temperature, ph = None, None

                for line in lines:
                    if "PH:" in line and "Temperature:" in line:
                        try:
                            ph = float(line.split("PH:")[1].split("Temperature:")[0].strip())
                            temperature = float(line.split("Temperature:")[1].strip())
                        except ValueError:
                            print("Error parsing pH or temperature value")

                if temperature is not None and ph is not None:
                    self.temp_label.configure(text=f"{temperature} °C")
                    self.ph_label.configure(text=f"{ph}")
                    self.timestamps.append(datetime.now().strftime("%I:%M %p"))
                    self.temperatures.append(temperature)
                    self.ph_values.append(ph)
            self.after(1000, read_serial)

        # Start the serial reading loop
        read_serial()

# Run the app
app = App()
app.mainloop()
