from tkinter import *
from PIL import Image, ImageTk, ImageFilter


class BlurredBackground:
    def __init__(self, root, img_path):
        self.root = root
        self.img_path = img_path
        self.root.title("Tic Tac Toe")

        # Bind the window resize event
        self.root.bind("<Configure>", self.resize_background)

        # Load and display the blurred background
        self.load_blurred_background()

    def load_blurred_background(self):
        # Open the image using PIL
        self.original_img = Image.open(self.img_path)

        # Display the image in its initial size (will resize as needed)
        self.display_background(self.original_img)

    def display_background(self, img):
        # Apply blur to the image
        blurred_img = img.filter(ImageFilter.GaussianBlur(5))

        # Convert the image to ImageTk format
        self.bg_photo = ImageTk.PhotoImage(blurred_img)

        # Create or update the background label
        if hasattr(self, 'background_label'):
            self.background_label.config(image=self.bg_photo)
        else:
            self.background_label = Label(self.root, image=self.bg_photo)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def resize_background(self, event):
        # Get the new window dimensions
        new_width = event.width
        new_height = event.height

        # Resize the original image to fit the new window size
        resized_img = self.original_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Update the background with the resized image
        self.display_background(resized_img)
