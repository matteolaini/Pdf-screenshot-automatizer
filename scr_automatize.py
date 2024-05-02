from pdf2image import convert_from_path
from PIL import Image, ImageTk, ImageGrab
import tkinter as tk
import os
import json
import PyPDF2
import cv2

#Class used to crop images manually (only when coordinates.json does not exist)
class ImageCropperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Cropper")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_frame, cursor="cross")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar_y = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollbar_x = tk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=2, ipadx=50)

        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.image_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.image_frame, anchor=tk.NW)


        self.image = None
        self.image_path = None
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

        self.zoom_in_button = tk.Button(self.root, text="Zoom In", command=self.zoom_in)
        self.zoom_in_button.pack()

        self.zoom_out_button = tk.Button(self.root, text="Zoom Out", command=self.zoom_out)
        self.zoom_out_button.pack()

        self.crop_button = tk.Button(self.root, text="Crop Image", command=self.crop_image)
        self.crop_button.pack()

        self.next_button = tk.Button(root, text="Next", command=self.next_image, justify=tk.RIGHT)
        self.next_button.pack()

        self.previous_button = tk.Button(root, text="Previous", command=self.prev_image, justify=tk.LEFT)
        self.previous_button.pack()

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.image_files = []
        self.current_image = None
        self.screenshot_coords = {}
        self.image_folder = tmpdir
        self.i=0;
        self.zoom_factor = 1.0

        # Get the list of image files in the folder
        self.image_files = [f for f in os.listdir(self.image_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]
        self.open_image(0)
        

    #Function to open the image corresponding to the index
    def open_image(self,index):
        self.current_image_index = index
        self.current_image = cv2.imread(os.path.join(tmpdir, self.image_files[index]))
        self.current_image_name = os.path.join(self.image_files[index])
        self.display_image()

    def next_image(self):
        # Load the next image
        if self.image_files.index(self.current_image_name) < len(self.image_files)-1:
            self.open_image((self.image_files.index(self.current_image_name) + 1))

    def prev_image(self):
        # Load the previous image
        if self.image_files.index(self.current_image_name) > 0:
            self.open_image((self.image_files.index(self.current_image_name) - 1))


    #Function to display the image on the canvas
    def display_image(self):
        if self.current_image is not None:
            image_rgb = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(image_rgb)
            resized_image = image_pil.resize((int(image_pil.width * self.zoom_factor), int(image_pil.height * self.zoom_factor)))
            self.image_tk = ImageTk.PhotoImage(resized_image)
            self.canvas.config(scrollregion=(0, 0, resized_image.width, resized_image.height))
            self.canvas.create_image(0, 0, image=self.image_tk, anchor=tk.NW)


    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")


    def on_mouse_move(self, event):
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)

    def on_button_release(self, event):
        pass


    def resize_image_canvas(self, event):
        self.image_canvas.config(scrollregion=self.image_canvas.bbox("all"))

    def zoom_in(self):
        self.zoom_factor *= 1.1
        self.display_image()

    def zoom_out(self):
        self.zoom_factor /= 1.1
        self.display_image()

    #Function to crop the image, based on the coordinates
    def crop_image(self):
        if self.start_x and self.end_x and self.start_y and self.end_y:
            x1 = int(min(self.start_x, self.end_x)/self.zoom_factor)
            x2 = int(max(self.start_x, self.end_x)/self.zoom_factor)
            y1 = int(min(self.start_y, self.end_y)/self.zoom_factor)
            y2 = int(max(self.start_y, self.end_y)/self.zoom_factor)
            self.cropped_image = self.current_image[y1:y2, x1:x2]
            self.screenshot_coords[self.i] = (self.current_image_index, x1, y1, x2, y2)
            self.save_image()

    #Function to save the cropped image in the screenshots folder
    def save_image(self):
        cv2.imwrite(os.path.join(screenshot_path, "screenshot_{}.png".format((self.i))), self.cropped_image)
        self.i+=1
        with open("coordinates.json", "w") as f:
            json.dump(self.screenshot_coords, f, indent=2)
        print("Cropped image saved successfully.")




#Main class
class PDFScreenshotApp:

    #Convert the pdf file to images
    def __init__(self, pdf_path):

        # Create a temporary folder to store the images
        self.root = tk.Tk()
        pdf = PyPDF2.PdfReader(pdf_path)

        # Get the number of pages in the PDF
        num_pages = len(pdf.pages)

        # Convert each page to an image
        for page in range(num_pages):
            image = convert_from_path(pdf_path, dpi=300, first_page=page+1, last_page=page+1)
            # Save the image to a file in the temporary folder
            image[0].save(os.path.join(tmpdir, f'output_{page+1}.png'), 'PNG')

        self.i=0;
        self.check_coordinates_file()

    
    #Function to check if coordinates file exists
    def check_coordinates_file(self):
        #If yes, crop automatically based on the saved coordinates
        if os.path.exists("coordinates.json"):
                self.crop_images()
        #Else, start the manual image cropper        
        else:
            self.start_image_cropper()

    #Function that takes screenshots automatically from all the images using coordinates
    def crop_images(self):
        with open("coordinates.json", "r") as file:
                self.coordinates = json.load(file)
        # Load the images from the temporary folder
        images = [f for f in os.listdir('temp_images') if f.endswith('.png')]

        # We store the cropped images in the folder named after the pdf in the screenshot path
        for key in self.coordinates:
            index, x1, y1, x2, y2 = self.coordinates[key]
            image = cv2.imread(os.path.join('temp_images', images[index]))
            crp_img = image[y1:y2, x1:x2]
            cv2.imwrite(os.path.join(screenshot_path, "screenshot_{}.png".format((self.i))), crp_img)
            self.i+=1

        #terminate the script
        self.root.destroy()


    #Function that starts the cropper
    def start_image_cropper(self):
        self.app = ImageCropperApp(self.root)
        self.root.mainloop()


#Starting code
if __name__ == "__main__":
    # Set up the folder path
    tmpdir = 'temp_images'
    folder_path = 'documents'
    screenshot_path = 'screenshots'

    # Get the only PDF file in the folder
    #REMEMBER: There must be only one PDF file in the folder, otherwise the script will not work
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    if len(pdf_files) != 1:
        print("Error: There must be exactly one PDF file in the folder")
        exit()
    pdf_file = os.path.join(folder_path, pdf_files[0])
    
    #Delete all files in the temp_images folder
    for file in os.listdir(tmpdir):
        os.remove(os.path.join(tmpdir, file))

    #Create a folder inside the screenshots folder, named after the pdf file
    screenshot_path = os.path.join(screenshot_path, pdf_files[0].split(".")[0])
    if not os.path.exists(screenshot_path):
        os.makedirs(screenshot_path)
    else:
        #delete all files in the folder
        for file in os.listdir(screenshot_path):
            os.remove(os.path.join(screenshot_path, file))
    
    app = PDFScreenshotApp(pdf_file)