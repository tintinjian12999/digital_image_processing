import ctypes
import cv2
import numpy as np
from ctypes import POINTER, c_ubyte, c_int
from tkinter import Tk, Button, Label, PhotoImage, filedialog
from PIL import Image, ImageTk

image_processing_lib = ctypes.CDLL('./main.so') # For Linux
#image_processing_lib = ctypes.CDLL('./main.dll') #For Windows

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

image_processing_lib.sobel_cpp.argtypes = [POINTER(c_ubyte),
                                                     POINTER(c_ubyte),
                                                     c_int,
                                                     c_int]
image_processing_lib.sobel_cpp.restype = None

image_processing_lib.fourier_sharp_cpp.argtypes = [POINTER(c_ubyte),
                                                     POINTER(c_ubyte),
                                                     c_int,
                                                     c_int]
image_processing_lib.fourier_sharp_cpp.restype = None

image_processing_lib.gaussian_blur_cpp.argtypes = [POINTER(c_ubyte),
                                                     POINTER(c_ubyte),
                                                     c_int,
                                                     c_int]
image_processing_lib.gaussian_blur_cpp.restype = None

image_processing_lib.gaussian_lowpass_cpp.argtypes = [POINTER(c_ubyte),
                                                     POINTER(c_ubyte),
                                                     c_int,
                                                     c_int]
image_processing_lib.gaussian_lowpass_cpp.restype = None
class ImageProcessorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Image Processor")

        self.image_label = Label(master, text="Original Image")
        self.image_label.grid(row=1, column=0, columnspan=3)

        self.processed_images = {'average': np.ones((300, 300), dtype=np.uint8) * 255,
                                 'median': np.ones((300, 300), dtype=np.uint8) * 255,
                                 'fourier': np.ones((300, 300), dtype=np.uint8) * 255,
                                 'sobel': np.ones((300, 300), dtype=np.uint8) * 255,
                                 'fourier_sharp': np.ones((300, 300), dtype=np.uint8) * 255,
                                 'gaussian_blur': np.ones((300, 300), dtype=np.uint8) * 255,
                                 'gaussian_lowpass': np.ones((300, 300), dtype=np.uint8) * 255,
                                 'empty0': np.ones((300, 300), dtype=np.uint8) * 255,
                                 'empty1': np.ones((300, 300), dtype=np.uint8) * 255,
                                 'empty2': np.ones((300, 300), dtype=np.uint8) * 255}


        self.processed_labels = {}

        self.init_images()

        self.load_button = Button(master, text="Open Image", command=self.load_image)
        self.load_button.grid(row=3, column=0, columnspan=2)

        self.smooth_button = Button(master, text="Smooth Filter", command=self.smooth_filter)
        self.smooth_button.grid(row=4, column=0, columnspan=2)

        self.average_button = Button(master, text="Sharp", command=self.sharp)
        self.average_button.grid(row=4, column=1, columnspan=2)

        self.lowpass_button = Button(master, text="Gaussian blur", command=self.gaussian_blur)
        self.lowpass_button.grid(row=5, column=0, columnspan=2)

        self.lowpass_button = Button(master, text="Gaussian lowpass", command=self.gaussian_lowpass)
        self.lowpass_button.grid(row=5, column=2, columnspan=2)

        self.lowpass_button = Button(master, text="clear", command=self.init_images)
        self.lowpass_button.grid(row=6, column=0)

    def init_images(self):
        self.image = np.ones((300, 300), dtype=np.uint8) * 255
        self.show_image()
        for method in self.processed_labels.keys():
            self.processed_images[method] = np.ones((300, 300), dtype=np.uint8) * 255
        self.show_processed_images(list(self.processed_labels.keys()))

    def show_image(self):
        if self.image is not None:
            img = Image.fromarray(self.image)
            img = ImageTk.PhotoImage(img)
            self.image_label.config(image=img)
            self.image_label.image = img

    def show_processed_images(self, method_set):
        for i, method in enumerate(method_set):
            processed_image = Image.fromarray(self.processed_images[method])
            processed_image = ImageTk.PhotoImage(processed_image)
            self.processed_labels[method].config(image=processed_image)
            self.processed_labels[method].image = processed_image

    def load_image(self):
        self.init_images()
        file_path = filedialog.askopenfilename(initialdir="./", title="Select file",
                                               filetypes=())
        if file_path:
            self.image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            if self.image.shape[0] % 2 == 1:
                self.image = cv2.resize(self.image, (self.image.shape[1], self.image.shape[0] - 1))
            if self.image.shape[1] % 2 == 1:
                self.image = cv2.resize(self.image, (self.image.shape[1] - 1, self.image.shape[0]))
            self.show_image()

    def smooth_filter(self):
        method_set = ['average', 'median', 'fourier']
        if self.image is not None: 
            for i, method in enumerate(['average', 'median', 'fourier']):
                label = Label(self.master, text=f"{method.capitalize()} Filter")
                col_num = 0 if i in [1] else 3
                label.grid(row=min(2, i + 1), column=col_num, columnspan=3)
                self.processed_labels[method] = label
            image_ptr = self.image.ctypes.data_as(POINTER(c_ubyte))
            output_median = np.ones_like(self.image) * 255
            output_median_ptr = output_median.ctypes.data_as(POINTER(c_ubyte))
            output_average = np.ones_like(self.image) * 255
            output_average_ptr = output_average.ctypes.data_as(POINTER(c_ubyte))
            output_fourier = np.ones_like(self.image) * 255
            output_fourier_ptr = output_fourier.ctypes.data_as(POINTER(c_ubyte))
            image_processing_lib.average_filter_cpp(image_ptr, output_average_ptr, self.image.shape[0],
                                                    self.image.shape[1])
            image_processing_lib.median_filter_cpp(image_ptr, output_median_ptr, self.image.shape[0],
                                                    self.image.shape[1])
            image_processing_lib.fourier_filter_cpp(image_ptr, output_fourier_ptr, self.image.shape[0],
                                                    self.image.shape[1])
            self.processed_images['median'] = output_median
            self.processed_images['fourier'] = output_fourier
            self.processed_images['average'] = output_average
            self.show_processed_images(method_set)
    def sharp(self):
        if self.image is not None:
            method_set = ['sobel', 'fourier_sharp']
            for i, method in enumerate(['sobel', 'fourier_sharp']):
                label = Label(self.master, text=f"{method.capitalize()} Filter")
                col_num = 0 if i in [0] else 3
                label.grid(row=2, column=col_num, columnspan=3)
                self.processed_labels[method] = label
            image_ptr = self.image.ctypes.data_as(POINTER(c_ubyte))
            output_sobel = np.ones_like(self.image) * 255
            output_sobel_ptr = output_sobel.ctypes.data_as(POINTER(c_ubyte))
            output_fourier_sharp = np.ones_like(self.image) * 255
            output_fourier_sharp_ptr = output_fourier_sharp.ctypes.data_as(POINTER(c_ubyte))
            image_processing_lib.sobel_cpp(image_ptr, output_sobel_ptr, self.image.shape[0],
                                                    self.image.shape[1])
            image_processing_lib.fourier_sharp_cpp(image_ptr, output_fourier_sharp_ptr, self.image.shape[0],
                                                    self.image.shape[1])
            self.processed_images['sobel'] = output_sobel
            self.processed_images['fourier_sharp'] = output_fourier_sharp
            self.show_processed_images(method_set)
    def gaussian_blur(self):
        if self.image is not None:
            method_set = ['gaussian_blur']
            for i, method in enumerate(['gaussian_blur']):
                label = Label(self.master, text=f"{method.capitalize()} Filter")
                col_num = 0 if i in [0] else 3
                label.grid(row=1, column=3, columnspan=3)
                self.processed_labels[method] = label
            image_ptr = self.image.ctypes.data_as(POINTER(c_ubyte))
            output_gaussian_blur = np.ones_like(self.image) * 255
            output_gaussian_blur_ptr = output_gaussian_blur.ctypes.data_as(POINTER(c_ubyte))
            image_processing_lib.gaussian_blur_cpp(image_ptr, output_gaussian_blur_ptr, self.image.shape[0],
                                                    self.image.shape[1])
            self.processed_images['gaussian_blur'] = output_gaussian_blur
            self.show_processed_images(method_set)
    def gaussian_lowpass(self):
        if self.image is not None:
            method_set = ['gaussian_lowpass']
            for i, method in enumerate(['gaussian_lowpass']):
                label = Label(self.master, text=f"{method.capitalize()} Filter")
                col_num = 0 if i in [0] else 3
                label.grid(row=1, column=3, columnspan=3)
                self.processed_labels[method] = label
            image_ptr = self.image.ctypes.data_as(POINTER(c_ubyte))
            output_gaussian_lowpass = np.ones_like(self.image) * 255
            output_gaussian_lowpass_ptr = output_gaussian_lowpass.ctypes.data_as(POINTER(c_ubyte))
            image_processing_lib.gaussian_lowpass_cpp(image_ptr, output_gaussian_lowpass_ptr, self.image.shape[0],
                                                    self.image.shape[1])
            self.processed_images['gaussian_lowpass'] = output_gaussian_lowpass
            self.show_processed_images(method_set)
if __name__ == "__main__":
    root = Tk()
    app = ImageProcessorGUI(root)
    root.mainloop()
