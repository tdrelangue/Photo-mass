import customtkinter as ctk
import tkinter as tk
import os
from PIL import Image
import batch
from icecream import ic

SHARP = 1
BRIGHT = 1
CONTR = 1
COL = 1


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.img = None
        self.image_ctk = None
        self.brightness = ctk.DoubleVar(value=1)
        self.sharpness = ctk.DoubleVar(value=1)
        self.color = ctk.DoubleVar(value=1)
        self.contrast = ctk.DoubleVar(value=1)

        self.title('Photo-mass')
        self.menubar = tk.Menu(master=self)
        self.file_menu = tk.Menu(master=self.menubar, tearoff=False)
        self.help_menu = tk.Menu(self.menubar, tearoff=False)
        self.path = "./images"
        self.pathOut = "./editedImages"
        self.minsize(600, 500)

        self.create_menu()

        # create a frame for params and image
        self.frame = ctk.CTkFrame(master=self)
        self.frame.pack()

        # tab view
        self.tab_view = ctk.CTkTabview(master=self.frame, anchor="w")
        self.tab_view.add("Brightness")
        self.tab_view.add("Sharpness")
        self.tab_view.add("Contrast")
        self.tab_view.add("Color")
        self.tab_view.pack(side='left')

        # Brightness
        self.brightness_label = ctk.CTkLabel(master=self.tab_view.tab("Brightness"),
                                             text="Brightness")
        self.brightness_label.pack()
        self.brightness_entry = ctk.CTkEntry(master=self.tab_view.tab("Brightness"),
                                             textvariable=self.brightness,
                                             state="disabled")
        self.brightness_entry.pack()

        self.brightness_slider = ctk.CTkSlider(master=self.tab_view.tab("Brightness"),
                                               from_=0,
                                               to=2,
                                               number_of_steps=100,
                                               command=self.brightness_slider_event)
        self.brightness_slider.pack(pady=20)

        # sharpness
        self.sharpness_label = ctk.CTkLabel(master=self.tab_view.tab("Sharpness"),
                                            text="Sharpness")
        self.sharpness_label.pack()
        self.sharpness_entry = ctk.CTkEntry(master=self.tab_view.tab("Sharpness"),
                                            textvariable=self.sharpness,
                                            state="disabled")
        self.sharpness_entry.pack()

        self.sharpness_slider = ctk.CTkSlider(master=self.tab_view.tab("Sharpness"),
                                              from_=0,
                                              to=2,
                                              number_of_steps=100,
                                              command=self.sharpness_slider_event)
        self.sharpness_slider.pack(pady=20)

        # Contrast
        self.contrast_label = ctk.CTkLabel(master=self.tab_view.tab("Contrast"),
                                           text="Contrast")
        self.contrast_label.pack()
        self.contrast_entry = ctk.CTkEntry(master=self.tab_view.tab("Contrast"),
                                           textvariable=self.contrast,
                                           state="disabled")
        self.contrast_entry.pack()

        self.contrast_slider = ctk.CTkSlider(master=self.tab_view.tab("Contrast"),
                                             from_=0,
                                             to=2,
                                             number_of_steps=100,
                                             command=self.contrast_slider_event)
        self.contrast_slider.pack(pady=20)

        # Color
        self.color_label = ctk.CTkLabel(master=self.tab_view.tab("Color"),
                                        text="Color")
        self.color_label.pack()
        self.color_entry = ctk.CTkEntry(master=self.tab_view.tab("Color"),
                                        textvariable=self.color,
                                        state="disabled")
        self.color_entry.pack()

        self.color_slider = ctk.CTkSlider(master=self.tab_view.tab("Color"),
                                          from_=0,
                                          to=2,
                                          number_of_steps=100,
                                          command=self.color_slider_event)
        self.color_slider.pack(pady=20)

        # image
        self.open_first_image(path=self.path)
        self.label = ctk.CTkLabel(master=self.frame, text="", image=self.image_ctk)
        self.label.pack()

        # validate parameters
        self.send_button = ctk.CTkButton(master=self, text="Validate parameters", command=self.send_button_click)
        self.send_button.pack(pady=20, side='bottom')

    # add methods to app
    def send_button_click(self):
        batch.batch_edit(self.sharpness.get(), self.brightness.get(), self.contrast.get(), self.color.get())

    def brightness_slider_event(self, value):
        self.brightness.set(round(value, 2))
        self.update_image()

    def sharpness_slider_event(self, value):
        self.sharpness.set(round(value, 2))
        self.update_image()

    def contrast_slider_event(self, value):
        self.contrast.set(round(value, 2))
        self.update_image()

    def color_slider_event(self, value):
        self.color.set(round(value, 2))
        self.update_image()

    def create_menu(self):
        # menu
        self.config(menu=self.menubar)

        # file menu
        self.file_menu.add_command(label='New')
        self.file_menu.add_command(label='Open...')
        self.file_menu.add_command(label='Close')
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label='Exit',
            command=self.destroy)

        # add the File menu to the menubar
        self.menubar.add_cascade(
            label="File",
            menu=self.file_menu)

        # create the Help menu
        self.help_menu.add_command(label='Welcome')
        self.help_menu.add_command(label='About...')

        # add the Help menu to the menubar
        self.menubar.add_cascade(
            label="Help",
            menu=self.help_menu
        )

    def open_first_image(self, path):
        filename = os.listdir(path)[0]
        self.img = Image.open(f"{path}/{filename}")
        self.image_output(self.img)

    def image_output(self, image):
        x, y = image.size
        rapport = x / y
        self.image_ctk = ctk.CTkImage(image.rotate(-90, expand=1), size=(300, 300 * rapport))

    def update_image(self):
        new = batch.edit(self.img, self.sharpness.get(), self.brightness.get(), self.contrast.get(), self.color.get())
        self.image_output(new)
        self.label.destroy()
        self.label = ctk.CTkLabel(master=self.frame, text="", image=self.image_ctk)
        self.label.pack()


app = App()
app.mainloop()
