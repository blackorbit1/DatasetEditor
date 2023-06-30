import os
import tkinter as tk
from PIL import Image, ImageTk

# Set the path to your dataset folder
dataset_path = "./100_style2"

# Get the list of image files and their corresponding caption files
image_files = [f for f in os.listdir(dataset_path) if f.endswith((".png", ".jpg", ".jpeg"))]
caption_files = [f for f in os.listdir(dataset_path) if f.endswith(".txt")]

# Create a dictionary to store image-caption pairs
image_caption_dict = {}
for image_file in image_files:
    image_name = os.path.splitext(image_file)[0]  # Extract the base filename without extension
    caption_file = image_name + ".txt"  # Construct the corresponding caption filename
    if caption_file in caption_files:
        with open(os.path.join(dataset_path, caption_file), "r") as f:
            caption = f.read().strip()
        image_caption_dict[image_file] = caption
    else:
        image_caption_dict[image_file] = ""  # Assign an empty string if caption file is not found

# Initialize variables
current_index = 0
total_images = len(image_files)

def save_caption():
    current_image = image_files[current_index]
    caption = caption_text.get("1.0", tk.END).strip()
    image_caption_dict[current_image] = caption
    with open(os.path.join(dataset_path, current_image.split(".")[0] + ".txt"), "w") as f:
        f.write(caption)

def previous_image():
    if current_index > 0:
        show_image(current_index - 1)

def update_caption():
    global current_index
    current_image = image_files[current_index]
    caption = image_caption_dict[current_image]
    caption_text.delete("1.0", tk.END)
    caption_text.insert(tk.END, caption)
    caption_text.configure(height=10)

def update_image():
    global current_index
    current_image = image_files[current_index]
    image = Image.open(os.path.join(dataset_path, current_image))
    image_width, image_height = image.size

    # Adjust the display width and height as per your preference
    display_width = 600
    display_height = 600

    aspect_ratio = min(display_width / image_width, display_height / image_height)
    new_width = int(image_width * aspect_ratio)
    new_height = int(image_height * aspect_ratio)
    image = image.resize((new_width, new_height), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    image_label.configure(image=photo)
    image_label.image = photo
    image_label.configure(borderwidth=10, relief="flat")

def update_file_label():
    global current_index
    current_image = image_files[current_index]
    file_label.configure(text=current_image)

def show_image(index):
    global current_index
    current_index = index
    update_caption()
    update_image()
    update_file_label()
    caption_text.focus_set()

def copy_file_name(event):
    root.clipboard_clear()
    root.clipboard_append(current_image)

# Create the main window
root = tk.Tk()
root.title("Image Browser")
root.bind("<Control-s>", lambda event: save_caption())
root.bind("<Alt-Left>", lambda event: show_image(current_index - 1))
root.bind("<Alt-Right>", lambda event: show_image(current_index + 1))

# Create the image label
image_label = tk.Label(root)
image_label.pack()

# Create the caption label
caption_text = tk.Text(root, height=3)
caption_text.pack()

# Create the file name label
current_image = image_files[current_index]
file_label = tk.Label(root, text=current_image)
file_label.pack()
file_label.bind("<Button-1>", copy_file_name)

# Set focus on caption field
caption_text.focus_set()

# Show the first image
show_image(current_index)

root.mainloop()