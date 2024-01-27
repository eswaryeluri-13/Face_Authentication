import cv2
import dlib
import numpy as np
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import face_recon
import home_page

first_blink=False
face_present=False

class BlinkDetectionApp:
    def __init__(self, master,username):
        self.username = username
        self.master = master
        self.master.title("Blink Detection App")

        self.cap = cv2.VideoCapture(0)  # 0 represents the default webcam
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        
        txt = 'hi, ' + username + '\n please blink your eyes under 10 seconds '
        self.message_label1 = tk.Label(self.master, text=txt, font=("Helvetica", 14))
        self.message_label1.pack(side=tk.TOP)
        
        self.canvas = tk.Canvas(self.master, width=640, height=480)
        self.canvas.pack()


        self.message_label = tk.Label(self.master, text="", font=("Helvetica", 14))
        self.message_label.pack(pady=10)



        self.btn_capture = tk.Button(self.master, text="Capture", command=self.capture, state=tk.DISABLED)
        self.btn_capture.pack(side=tk.RIGHT, padx=35, pady=10)

        self.btn_quit = tk.Button(self.master, text="Back", command=lambda : self.back_to_login(self.master))
        self.btn_quit.pack(side=tk.LEFT, padx=35, pady=10)

        self.EYE_AR_THRESH = 11
        self.EYE_AR_CONSEC_FRAMES = 1  # Change this to 1 to enable capture after a single blink
        self.COUNTER = 0
        self.capture_enabled = False
        self.run_time = 10 # Set the duration of video capture in seconds

        self.retry_window = None  # Retry window reference
        self.retry_message_var = tk.StringVar()

        self.start_blink_detection()
    def back_to_login(self):
        self.on_closing()
        home_page.create_username_entry_window()

    def start_blink_detection(self):
        self.check_blink()
        self.master.after(self.run_time * 1000, self.check_capture_status)

    def eye_aspect_ratio(self, eye):
        A = eye[1][1]
        B = eye[5][1]
        C = eye[2][0]
        D = eye[4][0]
        E = eye[0][1]
        F = eye[3][0]

        ear = (abs(C - E) + abs(D - F)) / (2.0 * abs(A - B))
        return ear

    def check_blink(self):
        global first_blink
        global face_present
        ret, frame = self.cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = self.detector(gray)
        
        if not faces:
            face_present=False
            self.display_frame(frame)
            self.btn_capture.config(state=tk.DISABLED)
            self.capture_enabled = False
            self.message_label.config(text="NO FACE FOUND")
        for face in faces:
            face_present=True
            self.message_label.config(text="FACE FOUND")
            if first_blink:
                self.btn_capture.config(state=tk.NORMAL)
                self.capture_enabled = True
            # Detect facial landmarks
            shape = self.predictor(gray, face)
            shape = [(shape.part(i).x, shape.part(i).y) for i in range(68)]

            # Extract the left and right eye coordinates
            left_eye = shape[42:48]
            right_eye = shape[36:42]

            # Compute the eye aspect ratio for left and right eyes
            left_ear = self.eye_aspect_ratio(left_eye)
            right_ear = self.eye_aspect_ratio(right_eye)

            # Average eye aspect ratio
            ear = (left_ear + right_ear) / 2.0

            # Check for eye blink
            # print(ear)
            if ear > self.EYE_AR_THRESH:
                print("Blinked")
                self.COUNTER += 1
                if self.COUNTER >= self.EYE_AR_CONSEC_FRAMES and not self.capture_enabled:
                    print("Blink detected! Enabling capture.")
                    self.btn_capture.config(state=tk.NORMAL)
                    self.capture_enabled = True
                    first_blink=True
            else:
                self.COUNTER = 0

            left_eye_np = np.array(left_eye, dtype=int)
            right_eye_np = np.array(right_eye, dtype=int)
            self.display_frame(frame, left_eye_np, right_eye_np)

        # Check for the 'q' key to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cap.release()
            cv2.destroyAllWindows()
            self.master.destroy()

        self.master.after(10, self.check_blink)


    def display_frame(self, frame, left_eye=None, right_eye=None):
        # Convert the frame to RGB for compatibility with Tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)
        photo = ImageTk.PhotoImage(image=image)

        # Update the canvas with the new frame
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.photo = photo  # To prevent garbage collection

        if left_eye is not None and right_eye is not None:
            # Flatten the list of eye coordinates
            left_eye_flat = [coord for point in left_eye for coord in point]
            right_eye_flat = [coord for point in right_eye for coord in point]

        # Draw eye polygons on the frame
            self.canvas.create_polygon(left_eye_flat, outline='green', fill='', width=1)
            self.canvas.create_polygon(right_eye_flat, outline='green', fill='', width=1)

    def capture(self):
        ret, frame = self.cap.read()

    # Save the captured image
        filename = f'test_image.jpg'
        cv2.imwrite(filename, frame)

    # Display the "Capture" message with an OK button
        # response = messagebox.askokcancel("Capture", f"Image captured and saved as {filename}. Click OK to close the application.")

    # Disable the capture button after capturing
        #self.btn_capture.config(state=tk.DISABLED)
        #self.capture_enabled = False

    # Close the main window if the user clicks OK
        # if response:
        #     self.on_closing()
        #     face_recon.main(filename,self.username)

        self.on_closing()
        face_recon.main(filename,self.username)
    def check_capture_status(self):
        if not self.capture_enabled:
            # Show retry window
            self.show_retry_window()

    def show_retry_window(self):
        global face_present
        print(face_present)
        if self.retry_window is None and face_present:
            response = messagebox.askokcancel("Warning", "No blink detected from the user\n click ok to retry")
            if response:
                self.retry_video()
            else:
                self.back_to_login()



            # self.retry_window = tk.Toplevel(self.master)
            # self.retry_window.title("Retry or Quit")

            # self.retry_message_var.set("No blink detected from the user.")

            # retry_label = tk.Label(self.retry_window, textvariable=self.retry_message_var)
            # retry_label.pack(pady=10)

            # retry_button = tk.Button(self.retry_window, text="Retry", command=self.retry_video)
            # retry_button.pack(side=tk.LEFT, padx=5, pady=10)

            # quit_button = tk.Button(self.retry_window, text="Quit", command=self.quit_application)
            # quit_button.pack(side=tk.RIGHT, padx=5, pady=10)
        else:
            self.retry_video()

    def retry_video(self):
        global first_blink
        # Close the retry window
        if self.retry_window:
            self.retry_window.destroy()
        self.retry_window = None
        if not first_blink:
            self.COUNTER = 0
            self.capture_enabled = False
            self.master.after(self.run_time * 1000, self.check_capture_status)
        # Reset counter and capture status
        self.COUNTER = 0
        self.capture_enabled = False

        # Disable the capture button
        #self.btn_capture.config(state=tk.DISABLED)
        

        # Start blink detection again
        #self.start_blink_detection()

    # def quit_application(self):
    #     # Close the retry window and main application
    #     if self.retry_window:
    #         self.retry_window.destroy()
    #     self.on_closing()

    def on_closing(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.master.destroy()

def main(username):
    root = tk.Tk()
    app = BlinkDetectionApp(root,username)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

# if __name__ == "__main__":
#     main()