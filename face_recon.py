import face_recognition
import os,sys
import tkinter as tk
from tkinter import messagebox
import live_image_blink

folder_path = r"C:\Users\eswar\Desktop\face_recog_final\data_base_images"

def recognize_face(test_encoding,username):
    global folder_path    
    persons = {}
    st = username + '.jpg'
    x1 = [os.path.join(folder_path, st)]
    persons[username] = x1

    print(persons)
        
    # Load the known images and encodings
    known_encodings = []
    known_names = []

    for name, image_files in persons.items():
        person_encodings = []
        for image_file in image_files:
            known_image = face_recognition.load_image_file(image_file)
            person_encodings.append(face_recognition.face_encodings(known_image)[0])
        known_encodings.append(person_encodings)
        known_names.append(name)

    # Set the tolerance parameter for face matchin
    tolerance = 0.6

    # Initialize variables for tracking the total confidence percentage and count of comparisons
    total_confidence_dict = {name: 0.0 for name in known_names}
    count_dict = {name: 0 for name in known_names}

    # Compare the test face encoding with the known face encodings
    for i, person_encodings in enumerate(known_encodings):
        for known_encoding in person_encodings:
            matches = face_recognition.compare_faces([known_encoding], test_encoding, tolerance=tolerance)
            if matches[0]:
                confidence_threshold = 0.55
                confidence = 1 - face_recognition.face_distance([known_encoding], test_encoding)[0]
                if confidence > confidence_threshold:
                    total_confidence_dict[known_names[i]] += confidence
                    count_dict[known_names[i]] += 1

    # Calculate the average confidence for each person
    average_confidence_dict = {}
    for name, total_confidence in total_confidence_dict.items():
        count = count_dict.get(name, 0)
        if count != 0:
            average_confidence = total_confidence / count
            average_confidence_dict[name] = average_confidence
    root = tk.Tk()
    root.withdraw() 
    # Display the result with the highest average confidence
    if not average_confidence_dict:
        response = messagebox.askokcancel("warning", "Face not matched with the username entered! \n  want to retry")
        if response:
            root.destroy()
            live_image_blink.main(username)
        else:
            root.destroy()

        print('No face detected in the captured image.')
    else:
        best_match_name = max(average_confidence_dict, key=average_confidence_dict.get)

        messagebox.showinfo("Login Successfull", "welcome "+best_match_name)
        root.destroy()
        print(f"Person {best_match_name} detected with average confidence: {average_confidence_dict[best_match_name] * 100:.2f}%")
        sys.exit(0)
    root.mainloop()
def main(filename,username):
    # frame = cv2.imread(filename)

    test_image = face_recognition.load_image_file(filename)
    test_encoding = face_recognition.face_encodings(test_image)
    root = tk.Tk()
    root.withdraw() 
    if not test_encoding:
        response = messagebox.askokcancel("warning", "No face detected in the captured image.")
        if response:
            root.destroy()
            live_image_blink.main(username)
        else:
            root.destroy()

        # print("No face detected in the captured image.")
    else:
        test_encoding = test_encoding[0]
    # Perform face recognition similar to your existing code
        recognize_face(test_encoding,username)
    root.mainloop()




