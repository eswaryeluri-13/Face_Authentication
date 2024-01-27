import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import face_recognition
import sqlite3
from tkinter import messagebox
import os
import home_page


class ImageCaptureApp:
    def start_taking_image(self):
        self.root = root = tk.Tk()
        self.root.title("Face Registering")
        print(self.USER_NAME)
        txt = self.USER_NAME +  ' ,Register Your Face'
        message_label = tk.Label(self.root, text=txt)
        message_label.pack(side=tk.TOP, pady=10)
        self.canvas = tk.Canvas(root)
        self.canvas.pack()

        self.capture_button = ttk.Button(root, text="Capture", command=self.capture_image)
        self.capture_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.next_button = ttk.Button(root, text="Cancel", command=lambda: self.return_to_login(self.root))
        self.next_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.video_capture = cv2.VideoCapture(0)  # Use 0 for the default camera
        self.update()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    def return_to_login(self,root):
        self.on_closing()
        home_page.main_page()

        

    def __init__(self):
        self.ALL_USERS = None
        self.USER_NAME = None
        self.create_table_if_not_exists()
        self.create_username_entry_window(self.start_application)


    def update(self):
        ret, frame = self.video_capture.read()

        if ret:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            photo = ImageTk.PhotoImage(image)

            self.canvas.config(width=image.width, height=image.height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo

        self.root.after(10, self.update)  # Update every 10 milliseconds

    def capture_image(self):
        ret, frame = self.video_capture.read()

        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            folder_path = r"C:\Users\eswar\Desktop\face_recog_final\data_base_images"  # Replace with the actual path to your folder
            os.makedirs(folder_path, exist_ok=True)
            file_name = os.path.join(folder_path, f"{self.USER_NAME}.jpg")
            pil_image.save(file_name)
        self.detect_face(file_name)

    def on_closing(self):
        self.video_capture.release()
        self.root.destroy()

    def detect_face(self, image_path):
        # Load the image
        image = cv2.imread(image_path)

        # Convert the image to grayscale for face detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Use a pre-trained face cascade classifier
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        # Check the conditions
        if len(faces) == 0:
            messagebox.showinfo("Warning", 'No face detected in the given image')
            os.remove(image_path)
            print("No face detected in the given image.")
        elif len(faces) > 1:
            messagebox.showinfo("Warning", "Only one face is allowed. Multiple faces detected")
            os.remove(image_path)
            print("Only one face is allowed. Multiple faces detected.")
        else:
            test_image = face_recognition.load_image_file(image_path)
            test_encoding = face_recognition.face_encodings(test_image)

            if not test_encoding:
                messagebox.showinfo("Warning", "No Face Detected")
                os.remove(image_path)
                print("No face detected in the captured image. Please try again.")
            else:
                
                another_window = tk.Toplevel(self.root)
                another_window.title("Face Id Confirmation")


                self.img = Image.open(image_path)
                self.tk_img = ImageTk.PhotoImage(self.img)

                # Create a label to display the image
                
                self.image_label = tk.Label(another_window, image=self.tk_img)
                self.image_label.pack()


                # Create buttons
                button1 = tk.Button(another_window, text="Register with this face", command=self.succesful_reg)
                button2 = tk.Button(another_window, text="Retry", command=lambda:self.retry_action(another_window,image_path))

                # Pack buttons at the bottom of the window
                button1.pack(side=tk.LEFT,padx=57,pady=10)
                button2.pack(side=tk.RIGHT,padx=75,pady=10)

                # Run the Tkinter event loop
                print('Face detected, and the image is clear.')

    def retry_action(self,root,path):
        os.remove(path)
        root.destroy()

    def succesful_reg(self):
        self.insert_username(self.USER_NAME)
        
        self.on_closing()
        home_page.main_page()

    def insert_username(self,username):
        # Connect to the SQLite database
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()

        # Insert a record into the Usernames table
        cursor.execute('''
            INSERT INTO Usernames (Username)
            VALUES (?)
        ''', (username,))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
    def start_application(self, username):
        
        print(f"Username entered: {username}")


        # Call your main application logic or open the main application window here

    def validate_username(self, username, next_button):
        if username:
            if self.check_username_exists(username):
                next_button["state"] = tk.DISABLED
                self.message_label.config(text='name already exist', fg='red')
            else:
                self.message_label.config(text='user name available', fg='green')
                next_button["state"] = tk.NORMAL
        else:
            next_button["state"] = tk.DISABLED

    def on_next(self, username_entry, on_next_callback, window):
        username = username_entry.get()
        if username:
            self.USER_NAME = username
            window.destroy()
            self.start_taking_image()
            on_next_callback(username)

    def create_username_entry_window(self, on_next_callback):
        def on_username_change(*args):
            self.validate_username(username_var.get(), next_button)

        root = tk.Tk()
        root.title("Username Entry")
        root.geometry('300x170')
        self.message_label = tk.Label(root, text="")
        self.message_label.pack(side=tk.BOTTOM,pady=10)


        username_var = tk.StringVar()

        username_label = ttk.Label(root, text="Enter Username:")
        username_label.pack(pady=10)

        username_entry = ttk.Entry(root, width=30, textvariable=username_var)
        username_entry.pack(pady=10)

        quick_button = ttk.Button(root, text="Back", command=lambda : self.back_to_login(root))
        quick_button.pack(pady=10, side=tk.LEFT,padx=25)
        next_button = ttk.Button(root, text="Next", command=lambda: self.on_next(username_entry, on_next_callback, root), state=tk.DISABLED)
        next_button.pack(pady=10, side=tk.RIGHT,padx=25)

        # Add a trace to call validate_username whenever the username entry changes
        username_var.trace_add("write", on_username_change)

        root.mainloop()

    def back_to_login(self,root):
        root.destroy()
        home_page.main_page()

    def create_table_if_not_exists(self):
        # Connect to the SQLite database
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()

        # Create the Usernames table if it does not exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usernames (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL UNIQUE
            )
        ''')

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
    def check_username_exists(self,username):
    # Connect to the SQLite database
        if  self.ALL_USERS is None:
    # Connect to the SQLite database
            conn = sqlite3.connect('your_database.db')
            cursor = conn.cursor()

            # Fetch all usernames from the Usernames table
            cursor.execute('SELECT Username FROM Usernames')
            result = cursor.fetchall()
            
            # Close the connection
            conn.close()
            if result is None:
                return False
            # Extract usernames from the result and return as a list
            self.ALL_USERS = [row[0] for row in result]
            print(self.ALL_USERS)
        return username in self.ALL_USERS
# if __name__ == "__main__":
#     ImageCaptureApp()
