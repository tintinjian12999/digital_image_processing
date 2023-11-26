#ifndef MAIN_H
#define MAIN_H
#include <stdio.h>
#include <opencv2/opencv.hpp>
using namespace cv;
extern "C" {

    void average_filter_cpp(const uchar* inputImage, uchar* outputImage, int rows, int cols);
    void median_filter_cpp(const uchar* inputImage, uchar* outputImage, int rows, int cols);
    void fourier_filter_cpp(const uchar* inputImage, uchar* outputImage, int rows, int cols);
    void sobel_cpp(const uchar* inputImage, uchar* outputImage, int rows, int cols);
    void fourier_sharp_cpp(const uchar* inputImage, uchar* outputImage, int rows, int cols);
    void gaussian_blur_cpp(const uchar* inputImage, uchar* outputImage, int rows, int cols);
    void gaussian_lowpass_cpp(const uchar* inputImage, uchar* outputImage, int rows, int cols);
    Mat shift(Mat img);

}
#endif
