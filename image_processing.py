import ctypes
import cv2
import numpy as np
from ctypes import POINTER, c_ubyte, c_int
from tkinter import Tk, Button, Label, PhotoImage, filedialog
from PIL import Image, ImageTk

image_processing_lib = ctypes.CDLL('./main.so')

image_processing_lib.average_filter_cpp.argtypes = [POINTER(c_ubyte),
                                                     POINTER(c_ubyte),
                                                     c_int,
                                                     c_int]
image_processing_lib.average_filter_cpp.restype = None

image_processing_lib.median_filter_cpp.argtypes = [POINTER(c_ubyte),
                                                    POINTER(c_ubyte),
                                                    c_int,
                                                    c_int]
image_processing_lib.median_filter_cpp.restype = None

image_processing_lib.fourier_filter_cpp.argtypes = [POINTER(c_ubyte),
                                                     POINTER(c_ubyte),
                                                     c_int,
                                                     c_int]
image_processing_lib.fourier_filter_cpp.restype = None


class ImageProcessorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Image Processor")

        self.image_label = Label(master, text="Original Image")
        self.image_label.grid(row=0, column=0, columnspan=2)

        self.processed_images = {'average': np.ones((300, 300), dtype=np.uint8) * 255,
                                 'median': np.ones((300, 300), dtype=np.uint8) * 255,
                                 'lowpass': np.ones((300, 300), dtype=np.uint8) * 255}

        self.processed_labels = {}
        for i, method in enumerate(['average', 'median', 'lowpass']):
            label = Label(master, text=f"{method.capitalize()} Filter")
            label.grid(row=i // 2 + 1, column=i % 2 * 2, columnspan=2)
            self.processed_labels[method] = label

        self.init_images()

        self.load_button = Button(master, text="Open Image", command=self.load_image)
        self.load_button.grid(row=3, column=0, columnspan=2)

        self.smooth_button = Button(master, text="Smooth Filter", command=self.median_image)
        self.smooth_button.grid(row=4, column=0)

        self.average_button = Button(master, text="Average Filter", command=self.average_image)
        self.average_button.grid(row=4, column=1)

        self.lowpass_button = Button(master, text="Lowpass Filter", command=self.lowpass_image)
        self.lowpass_button.grid(row=5, column=0, columnspan=2)

    def init_images(self):
        self.image = np.ones((300, 300), dtype=np.uint8) * 255
        self.show_image()
        for method in self.processed_images.keys():
            processed_image = np.ones((300, 300), dtype=np.uint8) * 255
            self.processed_images[method] = processed_image
            self.show_processed_images()

    def show_image(self):
        if self.image is not None:
            img = Image.fromarray(self.image)
            img = ImageTk.PhotoImage(img)
            self.image_label.config(image=img)
            self.image_label.image = img

    def show_processed_images(self):
        for i, method in enumerate(self.processed_images.keys()):
            processed_image = Image.fromarray(self.processed_images[method])
            processed_image = ImageTk.PhotoImage(processed_image)
            self.processed_labels[method].config(image=processed_image)
            self.processed_labels[method].image = processed_image

    def load_image(self):
        file_path = filedialog.askopenfilename(initialdir="./", title="Select file",
                                               filetypes=())
        if file_path:
            self.image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            self.show_image()

    def median_image(self):
        if self.image is not None:
            image_ptr = self.image.ctypes.data_as(POINTER(c_ubyte))

            output_median = np.ones_like(self.image) * 255
            output_median_ptr = output_median.ctypes.data_as(POINTER(c_ubyte))

            image_processing_lib.median_filter_cpp(image_ptr, output_median_ptr, self.image.shape[0],
                                                    self.image.shape[1])

            self.processed_images['median'] = output_median
            self.show_processed_images()

    def average_image(self):
        if self.image is not None:
            image_ptr = self.image.ctypes.data_as(POINTER(c_ubyte))
            output_average = np.ones_like(self.image) * 255
            output_average_ptr = output_average.ctypes.data_as(POINTER(c_ubyte))

            image_processing_lib.average_filter_cpp(image_ptr, output_average_ptr, self.image.shape[0],
                                                    self.image.shape[1])

            self.processed_images['average'] = output_average
            self.show_processed_images()

    def lowpass_image(self):
        if self.image is not None:
            image_ptr = self.image.ctypes.data_as(POINTER(c_ubyte))
            if self.image.shape[0] % 2 == 1:
                self.image = cv2.resize(self.image, (self.image.shape[1], self.image.shape[0] - 1))
            if self.image.shape[1] % 2 == 1:
                self.image = cv2.resize(self.image, (self.image.shape[1] - 1, self.image.shape[0]))
            output_fourier = np.ones_like(self.image) * 255
            output_fourier_ptr = output_fourier.ctypes.data_as(POINTER(c_ubyte))

            image_processing_lib.fourier_filter_cpp(image_ptr, output_fourier_ptr, self.image.shape[0],
                                                    self.image.shape[1])

            self.processed_images['fourier'] = output_fourier
            self.show_processed_images()


if __name__ == "__main__":
    root = Tk()
    app = ImageProcessorGUI(root)
    root.mainloop()

