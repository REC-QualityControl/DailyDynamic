import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class ImageViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Viewer")
        self.geometry("1400x800")
        self.current_folder_index = 0
        # self.current_filter_index = 0
        self.current_image_index = 0
        self.current_dir_index=0
        self.image_extensions = (".jpg", ".jpeg", ".png", ".gif")
        self.filter_check = tk.BooleanVar()
        self.load_dirs()
        self.load_folders()
        self.create_widgets()
        self.load_images()

    def load_folders(self):
        self.folder_path = os.path.join(self.dir_path, self.dir_list[self.current_dir_index])
        # print(os.listdir(self.folder_path))
        # self.folder_path = "C:/Users/RECONNECT/Downloads/plots-20230925T082303Z-001/plots/"  # Change this to your desired folder path
        self.folder_list = sorted(
            [f for f in os.listdir(self.folder_path) if os.path.isdir(os.path.join(self.folder_path, f))]
        )
        self.filtered_folder_list = self.folder_list[:]
        print(self.current_dir_index)
        print(self.folder_path)

    def load_dirs(self):
        self.dir_path = "C:\\Users\\RECONNECT\\Documents\\Plots"  # Change this to your desired folder path
        self.dir_list = sorted(
            [f for f in os.listdir(self.dir_path) if os.path.isdir(os.path.join(self.dir_path, f))]
        )
    
    def load_images(self):
        folder_name = self.filtered_folder_list[self.current_folder_index]
        folder_path = os.path.join(self.folder_path, folder_name)
        image_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(self.image_extensions)])
        if image_files:
            self.image_list = [os.path.join(folder_path, image_file) for image_file in image_files]
            self.show_image()

    def show_image(self):
        image_path = self.image_list[self.current_image_index]
        img = Image.open(image_path)
        img = img.resize((1200, 700), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.photo)

    def update_image(self, direction):
        self.current_image_index += direction
        if self.current_image_index >= len(self.image_list):
            self.current_image_index = 0
        elif self.current_image_index < 0:
            self.current_image_index = len(self.image_list) - 1
        self.show_image()

    def update_folder(self, direction):
        self.current_folder_index += direction
        if self.current_folder_index >= len(self.filtered_folder_list):
            self.current_folder_index = 0
        elif self.current_folder_index < 0:
            self.current_folder_index = len(self.filtered_folder_list) - 1
        self.load_images()
    
    def update_dir(self, direction):
        self.current_dir_index += direction
        if self.current_dir_index >= len(self.dir_list):
            self.current_dir_index = 0
        elif self.current_dir_index < 0:
            self.current_dir_index = len(self.dir_list) - 1
        self.load_folders()
        self.load_images()


    def filter_folders(self):
        if(self.filter_check.get() == 1):
        # filter_text = self.filter_entry.get().lower()
            filter_text = "ctrl"
            self.filtered_folder_list = [folder for folder in self.folder_list if filter_text in folder.lower()]
        elif(self.filter_check.get() == 0):
            self.load_folders()
        self.load_images()

    def create_widgets(self):
        self.image_label = ttk.Label(self,text = 'label', width=600)
        self.image_label.pack()

        tk.Button(self, bg='green', text = 'PORTDIS').pack(side = tk.RIGHT)
        tk.Button(self, bg='yellow', text = 'GRIDCRT').pack(side = tk.RIGHT)
        tk.Button(self, bg='blue', text = 'UNRPAVC').pack(side = tk.RIGHT)
        tk.Button(self, bg='red', text = 'TIME_DRIFT').pack(side = tk.RIGHT)
        tk.Button(self, bg='orange', text = 'MISMATCH').pack(side = tk.RIGHT)

        prev_ss_button = ttk.Button(self, text = "Prev Substation", command = lambda: self.update_dir(-1))
        prev_ss_button.pack(side = tk.LEFT, padx=10, pady=10)

        prev_folder_button = ttk.Button(self, text="Prev Folder", command=lambda: self.update_folder(-1))
        prev_folder_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        prev_button = ttk.Button(self, text="Prev Image", command=lambda: self.update_image(-1))
        prev_button.pack(side=tk.LEFT, padx=10, pady=10)

        next_button = ttk.Button(self, text="Next Image", command=lambda: self.update_image(1))
        next_button.pack(side=tk.LEFT, padx=10, pady=10)

        next_folder_button = ttk.Button(self, text="Next Folder", command=lambda: self.update_folder(1))
        next_folder_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        next_ss_button = ttk.Button(self, text = "Next Substation", command = lambda : self.update_dir(1))
        next_ss_button.pack(side = tk.LEFT, padx=10, pady=10)

        # self.filter_entry = ttk.Entry(self, width=20)
        # self.filter_entry.pack(side=tk.LEFT, padx=10, pady=10)

        # filter_button = ttk.Button(self, text="Filter", command=self.filter_folders)
        # filter_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.filter_button = ttk.Checkbutton(self, text="CTRL", variable=self.filter_check, command=lambda: self.filter_folders())
        self.filter_button.pack(side = tk.LEFT, padx=10, pady=10)

        self.bind('<Left>', lambda event: self.update_folder(-1))
        self.bind('<Right>', lambda event: self.update_folder(1))
        self.bind('<Up>', lambda event: self.update_dir(-1))
        self.bind('<Down>', lambda event: self.update_dir(1))


if __name__ == "__main__":
    app = ImageViewer()
    app.mainloop()
