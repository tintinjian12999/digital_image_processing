#include <iostream>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

//平移遮罩圖片
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

int main() {
    //為了能完整平移圖片需要偶數
	Mat img = imread("./Figure_1.jpg", IMREAD_GRAYSCALE);
	if (img.rows % 2 == 1)
		resize(img, img, Size(img.cols, img.rows - 1));
	if (img.cols % 2 == 1)
		resize(img, img, Size(img.cols - 1, img.rows));

	Mat dftInput1, dftImage1, inverseDFT, inverseDFTconverted; //新建轉換所需的容器
	img.convertTo(dftInput1, CV_32F); //將原圖轉換成可計算矩陣容器
	dft(dftInput1, dftImage1, DFT_COMPLEX_OUTPUT);    //進行 DFT
    
    //遮罩建立 (低通濾波)
    Mat filter = getGaussianKernel(5, 0.5, CV_32F) * getGaussianKernel(5, 0.5, CV_32F).t();

    // 創建全為1的遮罩
    //Mat filter(Size(img.cols, img.rows), CV_32F, Scalar::all(1));

    // 將遮罩和高斯核相乘
    //filter = filter.mul(gaussian);
	filter = shift(filter); //平移遮罩

    //進行低通濾波
	Mat dftImage1_vector(filter.size(), CV_32F, dftImage1.data);
	dftImage1_vector = dftImage1_vector.mul(filter);
	imshow("dftImage1_vector", dftImage1_vector); //查看遮罩位置

	// 重建圖型
	idft(dftImage1, inverseDFT, DFT_SCALE | DFT_REAL_OUTPUT); //進行 IDFT
	inverseDFT.convertTo(inverseDFTconverted, CV_8U);
	imshow("Output", inverseDFTconverted);

	imshow("Original Image", img);
	waitKey(0);
	}
