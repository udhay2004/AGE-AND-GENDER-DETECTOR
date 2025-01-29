import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
from keras.models import load_model

# Load the trained model
model = load_model('C:\\Users\\udhay\\Downloads\\Age_Sex_Detection.keras')

# Initialize the main window
top = tk.Tk()
top.geometry('800x600')
top.title('Age & Gender Detector')
top.configure(background="#CDCDCD")

# Create labels for age & gender
label1 = tk.Label(top, background="#CDCDCD", font=('arial', 15, "bold"))
label2 = tk.Label(top, background="#CDCDCD", font=('arial', 15, "bold"))
sign_image = tk.Label(top)

def Detect(file_path):
    """Perform age and gender detection."""
    try:
        image = Image.open(file_path).convert("RGB")  # Ensure RGB format
        image = image.resize((48, 48))  # Resize correctly
        image = np.array(image) / 255.0  # Normalize pixel values
        image = np.expand_dims(image, axis=0)  # Reshape to match model input (1, 48, 48, 3)

        # Predict gender & age
        pred = model.predict(image)
        age = int(np.round(pred[1][0]))  # Age prediction
        sex = int(np.round(pred[0][0]))  # Gender prediction

        sex_f = ["Male", "Female"]
        
        print(f"PREDICTED AGE: {age}")
        print(f"PREDICTED GENDER: {sex_f[sex]}")

        label1.configure(foreground="#011638", text=f"Predicted Age: {age}")
        label2.configure(foreground="#011638", text=f"Predicted Gender: {sex_f[sex]}")

    except Exception as e:
        print(f"Error in detection: {e}")

def show_Detect_button(file_path):
    """Create and display the detect button."""
    Detect_b = tk.Button(top, text="Detect Image", command=lambda: Detect(file_path), padx=10, pady=5)
    Detect_b.configure(background="#364156", foreground="white", font=("arial", 10, "bold"))
    Detect_b.place(relx=0.79, rely=0.46)

def upload_image():
    """Allow the user to upload an image."""
    try:
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        uploaded = Image.open(file_path)
        uploaded.thumbnail((top.winfo_width()/2.25, top.winfo_height()/2.25))  # Adjust thumbnail size
        im = ImageTk.PhotoImage(uploaded)

        sign_image.configure(image=im)
        sign_image.image = im
        label1.configure(text='')
        label2.configure(text='')
        show_Detect_button(file_path)

    except Exception as e:
        print(f"Error uploading image: {e}")

# Upload Button
upload_button = tk.Button(top, text="Upload an Image", command=upload_image, padx=10, pady=5)
upload_button.configure(background="#364156", foreground='white', font=('arial', 10, 'bold'))
upload_button.pack(side='bottom', pady=50)

# Display elements
sign_image.pack(side='bottom', expand=True)
label1.pack(side="bottom", expand=True)
label2.pack(side="bottom", expand=True)

# App Heading
heading = tk.Label(top, text="Age and Gender Detector", pady=20, font=('arial', 20, 'bold'))
heading.configure(background="#CDCDCD", foreground="#364156")
heading.pack()

top.mainloop()
