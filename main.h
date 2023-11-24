#ifndef MAIN_H
#define MAIN_H
#include <stdio.h>
#include <opencv2/opencv.hpp>
using namespace cv;

Mat average_filter(const Mat& inputImage);
Mat median_filter(const Mat& inputImage);
Mat fourier_filter(Mat inputImage);
Mat shift(Mat img);

#endif
