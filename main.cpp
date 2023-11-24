
#include "main.h"
int main(int argc, char* argv[]) {

    // 檢查是否有指定輸入影像檔案
    if ( argc != 2 ) {
      printf("usage: DisplayImage.out <Image_Path>n");
      return -1;
    }
    // 讀取影像檔案
    Mat image;
    image = imread(argv[1], 0);
    if ( !image.data ) {
      printf("No image data n");
      return -1;
    }
    imshow("原始影像", image);
    Mat averagedImage;
    averagedImage = average_filter(image);
    Mat medianImage;
    medianImage = median_filter(image);
    Mat fourier_filterImage;
    fourier_filterImage = fourier_filter(image);
    imshow("平均濾波後的影像", averagedImage);
    imshow("中值濾波後的影像", medianImage);
    imshow("傅立葉濾波後的影像", fourier_filterImage);
    waitKey(0);

    destroyAllWindows();  
    return 0;
}

Mat average_filter(const Mat& inputImage)
{
	Mat averagedImage;
    blur(inputImage, averagedImage, Size(3, 3));  
    return averagedImage;
}
Mat median_filter(const Mat& inputImage)
{
	Mat medianImage;
    medianBlur(inputImage, medianImage, 3); 
    return medianImage;
}
Mat fourier_filter(Mat inputImage)
{
	if (inputImage.rows % 2 == 1)
		resize(inputImage, inputImage, Size(inputImage.cols, inputImage.rows - 1));
	if (inputImage.cols % 2 == 1)
		resize(inputImage, inputImage, Size(inputImage.cols - 1, inputImage.rows));

	Mat dftInput1, dftImage1, inverseDFT, inverseDFTconverted; 
	inputImage.convertTo(dftInput1, CV_32F); 
	dft(dftInput1, dftImage1, DFT_COMPLEX_OUTPUT);    
    
	Mat filter(Size(inputImage.cols, inputImage.rows), CV_32F, Scalar::all(0));
	int half_x = filter.cols / 2;
	int half_y = filter.rows / 2;
	int radius = 150; 
	for (int a = 0; a < filter.rows; a++) {
		for (int b = 0; b < filter.cols; b++) {
			if (pow((a - half_y), 2) + pow((b - half_x), 2) < pow(radius,2)) {
				filter.at<float>(a, b) = 1;
			}
		}
	}
	filter = shift(filter);
	Mat dftImage1_vector(filter.size(), CV_32F, dftImage1.data);
	dftImage1_vector = dftImage1_vector.mul(filter);
	imshow("dftImage1_vector", dftImage1_vector); 

	idft(dftImage1, inverseDFT, DFT_SCALE | DFT_REAL_OUTPUT); 
	inverseDFT.convertTo(inverseDFTconverted, CV_8U);
	return  inverseDFTconverted;
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
