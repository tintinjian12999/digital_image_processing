
#include "main.h"
extern "C" {
void average_filter_cpp(const uchar* inputImage, uchar* outputImage, int rows, int cols) {
    Mat inputMat(rows, cols, CV_8UC1, const_cast<uchar*>(inputImage));
    Mat outputMat(rows, cols, CV_8UC1, outputImage);
    blur(inputMat, outputMat,Size(3, 3));
    outputMat.copyTo(cv::Mat(rows, cols, CV_8UC1, outputImage));
}

void median_filter_cpp(const uchar* inputImage, uchar* outputImage, int rows, int cols) {
    Mat inputMat(rows, cols, CV_8UC1, const_cast<uchar*>(inputImage));
    Mat outputMat(rows, cols, CV_8UC1, outputImage);
    medianBlur(inputMat, outputMat, 3);
    outputMat.copyTo(cv::Mat(rows, cols, CV_8UC1, outputImage));
}

void fourier_filter_cpp(const uchar* inputImage, uchar* outputImage, int rows, int cols) {
    Mat inputMat(rows, cols, CV_8UC1, const_cast<uchar*>(inputImage));
    Mat outputMat(rows, cols, CV_8UC1, outputImage);

	Mat dftInput1, dftImage1, inverseDFT; //新建轉換所需的容器
	inputMat.convertTo(dftInput1, CV_32F); //將原圖轉換成可計算矩陣容器
	dft(dftInput1, dftImage1, DFT_COMPLEX_OUTPUT);    //進行 DFT
	    //遮罩建立 (低通濾波)
	Mat filter(Size(inputMat.cols, inputMat.rows), CV_32F, Scalar::all(0));
	int half_x = filter.cols / 2;
	int half_y = filter.rows / 2;
	int radius = 150; //遮罩半徑
	for (int a = 0; a < filter.rows; a++) {
		for (int b = 0; b < filter.cols; b++) {
			if (pow((a - half_y), 2) + pow((b - half_x), 2) < pow(radius,2)) {
				filter.at<float>(a, b) = 1;
			}
		}
	}
	filter = shift(filter); //平移遮罩
	//進行低通濾波
	Mat dftImage1_vector(filter.size(), CV_32F, dftImage1.data);
	dftImage1_vector = dftImage1_vector.mul(filter);
	idft(dftImage1, inverseDFT, DFT_SCALE | DFT_REAL_OUTPUT); //進行 IDFT
	inverseDFT.convertTo(outputMat, CV_8UC1);
	outputMat.copyTo(Mat(rows, cols, CV_8UC1, outputImage));
}

Mat shift(Mat img) {
	int row = img.rows / 2;
	int col = img.cols / 2;
	Mat q1(img, Rect(0, 0, col, row));
	Mat q2(img, Rect(col, 0, col, row));
	Mat q3(img, Rect(0, row, col, row));
	Mat q4(img, Rect(col, row, col, row));
	Mat tmp;
	q1.copyTo(tmp);
	q4.copyTo(q1);
	tmp.copyTo(q4);

	q3.copyTo(tmp);
	q2.copyTo(q3);
	tmp.copyTo(q2);
	return img;
}



}
