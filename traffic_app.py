import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import os
import time
import logging
import cv2
from ultralytics import YOLO
import green_time_signal

# --- Logging setup
logging.basicConfig(filename="traffic_app.log",
                    level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# --- UI Colors
BG_COLOR = "#f9f9f9"
PRIMARY_COLOR = "#2E7D32"
BTN_COLOR = "#4CAF50"
TEXT_COLOR = "black"
FONT_FAMILY = "Helvetica"

class TrafficApp:
    def __init__(self, root):   # <-- FIXED here: was _init_ before
        self.root = root
        self.model = None
        self.flashing = False

        self.root.title("Smart Traffic Management")
        self.root.configure(bg=BG_COLOR)
        self.root.geometry("400x600")
        self.show_login_screen()

    def show_login_screen(self):
        self.clear_root()
        self.login_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.login_frame.pack(expand=True)

        tk.Label(self.login_frame, text="Login", font=(FONT_FAMILY, 20, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=10)
        tk.Label(self.login_frame, text="Username", font=(FONT_FAMILY, 12), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=5)
        self.username_entry = tk.Entry(self.login_frame, font=(FONT_FAMILY, 12))
        self.username_entry.pack(pady=5)
        tk.Label(self.login_frame, text="Password", font=(FONT_FAMILY, 12), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*", font=(FONT_FAMILY, 12))
        self.password_entry.pack(pady=5)
        tk.Button(self.login_frame, text="Login", bg=BTN_COLOR, fg="white", font=(FONT_FAMILY, 12),
                  command=self.check_login).pack(pady=15)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "admin" and password == "traffic123":
            logging.info("Login successful")
            self.setup_main_window()
        else:
            messagebox.showerror("Error", "Invalid username or password")
            logging.warning("Login failed")

    def setup_main_window(self):
        self.clear_root()
        self.root.title("Smart Traffic Management - Main")

        tk.Label(self.root, text="Smart Traffic Management", font=(FONT_FAMILY, 18, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=15)

        self.upload_btn = tk.Button(self.root, text="Upload Image", bg=BTN_COLOR, fg="white", font=(FONT_FAMILY, 12),
                                    command=self.upload_image)
        self.upload_btn.pack(pady=10)

        # Traffic light frame
        self.traffic_frame = tk.Frame(self.root, bg=BG_COLOR, bd=2, relief="groove")
        self.traffic_frame.pack(pady=20)

        tk.Label(self.traffic_frame, text="Traffic Light", font=(FONT_FAMILY, 14, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=5)

        self.canvas = tk.Canvas(self.traffic_frame, width=100, height=220, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack()
        self.red_light = self.canvas.create_oval(30, 20, 70, 60, fill="grey")
        self.yellow_light = self.canvas.create_oval(30, 90, 70, 130, fill="grey")
        self.green_light = self.canvas.create_oval(30, 160, 70, 200, fill="grey")

        # Small progress bar
        self.progress_canvas = tk.Canvas(self.root, width=300, height=10, bg="#e0e0e0", highlightthickness=0)
        self.progress_canvas.pack(pady=10)
        self.progress_bar = self.progress_canvas.create_rectangle(0, 0, 0, 10, fill=BTN_COLOR)

        # Results
        self.result_label = tk.Label(self.root, text="", font=(FONT_FAMILY, 12), bg=BG_COLOR, fg=TEXT_COLOR, justify="center")
        self.result_label.pack(pady=15)

        self.load_model()

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def load_model(self):
        logging.info("Loading YOLO model")
        try:
            self.model = YOLO("yolov8l.pt")
            logging.info("Model loaded successfully")
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            messagebox.showerror("Error", "Failed to load YOLO model")
            self.root.quit()

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("JPEG files", ".jpg;.jpeg")])
        if not file_path:
            return
        self.process_image(file_path)

    def update_progress(self, progress):
        width = 300 * progress
        self.progress_canvas.coords(self.progress_bar, 0, 0, width, 10)
        self.root.update()

    def process_image(self, file_path):
        logging.info(f"Processing image: {file_path}")
        self.set_light("red")
        self.result_label.config(text="Processing Image...", fg=TEXT_COLOR)
        self.update_progress(0)
        self.root.update()

        # Simulated progress
        for i in range(1, 11):
            self.update_progress(i / 10)
            time.sleep(0.2)

        vehicle_count = self.detect_vehicles(file_path)
        if vehicle_count is None:
            self.set_light("off")
            self.update_progress(0)
            messagebox.showwarning("Warning", "No vehicles detected.")
            return

        green_time = green_time_signal.adjust_green_signal_time(vehicle_count)
        result_text = f"Detected Vehicles: {vehicle_count}\nGreen Signal Time: {green_time} seconds"

        # Red pause
        self.set_light("red")
        self.root.update()
        time.sleep(1)

        # Yellow pause
        self.set_light("yellow")
        self.root.update()
        time.sleep(2)

        # Green light and show result
        self.set_light("green")
        self.result_label.config(text=result_text, fg=TEXT_COLOR)
        self.root.update()

        # Reset after green_time
        self.root.after(int(green_time * 1000), self.reset_lights)

    def set_light(self, color):
        colors = {"red": "grey", "yellow": "grey", "green": "grey"}
        if color in colors:
            colors[color] = color
        self.canvas.itemconfig(self.red_light, fill=colors["red"])
        self.canvas.itemconfig(self.yellow_light, fill=colors["yellow"])
        self.canvas.itemconfig(self.green_light, fill=colors["green"])

    def reset_lights(self):
        self.set_light("off")
        self.update_progress(0)
        self.result_label.config(text="", fg=TEXT_COLOR)

    def detect_vehicles(self, image_path):
        try:
            image = cv2.imread(image_path)
            if image is None:
                return None

            image = cv2.convertScaleAbs(image, alpha=1.2, beta=10)
            height, width = image.shape[:2]
            max_w, max_h = 1280, 720
            scale = min(max_w / width, max_h / height, 1.0)
            image = cv2.resize(image, (int(width * scale), int(height * scale)))

            results = self.model(image, conf=0.5, iou=0.7)
            vehicle_count = 0
            for result in results:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    if class_id in [2, 3, 5, 7]:
                        vehicle_count += 1

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            output_dir = "images"
            os.makedirs(output_dir, exist_ok=True)
            output_image = os.path.join(output_dir, f"output_{timestamp}.jpg")
            cv2.imwrite(output_image, image)

            with open("vehicle_count.txt", "w") as f:
                f.write(str(vehicle_count))

            return vehicle_count
        except Exception as e:
            logging.error(f"Detection error: {e}")
            return None

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = TrafficApp(root)
        root.mainloop()
    except Exception as e:
        logging.error(f"Error in main: {e}")
