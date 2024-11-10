import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageFont, ImageDraw

class WatermarkAdder:
    def __init__(self, root):
        """
        Construct a WatermarkAdder.

        Parameters
        ----------
        root : tkinter.Tk
            The root window to construct the GUI in.
        """
        self.root = root
        self.root.config(padx=10, pady=10)
        self.root.geometry("300x200")
        self.root.title("Watermark Adder")

        # Create a label and button to select an image
        self.image_label = tk.Label(root, 
                                    text="Select an image:",  
                                    font=("Arial", 10),
                                    pady=10)
        self.image_label.pack()

        self.image_button = tk.Button(root, 
                                      text="Browse", 
                                      command=self.select_image,  
                                      font=("Arial", 10))
        self.image_button.pack()

        # Create a label and entry to input watermark text
        self.watermark_label = tk.Label(root, 
                                        text="Enter watermark text:",  
                                        font=("Arial", 10),
                                        pady=10)
        self.watermark_label.pack()

        self.watermark_entry = tk.Entry(root)
        self.watermark_entry.pack()

        # Create a button to add watermark
        self.add_watermark_button = tk.Button(root, 
                                              text="Add Watermark", 
                                              command=self.add_watermark,  
                                              font=("Arial", 10))
        self.add_watermark_button.pack()

        self.image_path = None  # Initialize image_path

    def select_image(self):
        # Open file dialog to select an image
        image_path = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg .jpeg .png .bmp")])
        self.image_path = image_path
        if self.image_path:
            self.watermark_entry.focus_set()

    def show_popup(self, title, message):
        """
        Show a pop-up window with the given title and message.
        """
        popup = tk.Toplevel(self.root)
        popup.config(padx=10, pady=10)
        popup.title(title)
        popup.geometry("400x150")
        label = tk.Label(popup, text=message, pady=20, padx=10)
        label.pack()
        ok_button = tk.Button(popup, text="OK", command=popup.destroy, padx=30, pady=5)
        ok_button.pack()
        popup.transient(self.root)  # Keep the popup on top of the main window
        popup.grab_set()            # Make the popup modal

    def add_watermark(self):
        if not self.image_path:
            self.show_popup("Error", "No image selected!")
            return

        try:
            # Open the selected image
            image = Image.open(self.image_path).convert("RGBA")
            suff = self.image_path.split(sep='.')[-1]  # Get the image suffix
            original_dir = self.image_path.split(sep='/')[:-1]
            original_dir = '/'.join(original_dir)  # Get the original directory

            # Get the watermark text
            watermark_text = self.watermark_entry.get()

            if not watermark_text:
                self.show_popup("Error", "Watermark text cannot be empty!")
                return

            watermark_txt = Image.new('RGBA', image.size, (255, 255, 255, 0))

            # Set the font and font size
            font = ImageFont.truetype("arial.ttf", 100)

            # Create a drawing context
            draw = ImageDraw.Draw(image)

            # Calculate text size using textbbox
            text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            # Position at the bottom right
            padding = 15  # Padding from the edges
            text_position = (image.width - text_width - padding, image.height - text_height - (padding + 10))

            # Draw the watermark text
            draw.text(text_position, watermark_text, font=font, fill=(255, 255, 255, 100))

            # Save the watermarked image
            combined = Image.alpha_composite(image, watermark_txt)
            save_path = f"""{original_dir}/{self.image_path.split(sep='/')[-1].removesuffix(f".{suff}")}_watermarked_image.png"""
            combined.save(save_path)

            # Show a success message
            self.show_popup("Success", f"Watermarked image saved at:\n{save_path}")
            
            # Clear the inputs after successful processing
            self.image_path = None
            self.watermark_entry.delete(0, tk.END)

        except Exception as e:
            self.show_popup("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkAdder(root)
    root.mainloop()
