#include <opencv2/opencv.hpp>

class WebcamRecorder {
public:
    explicit WebcamRecorder(const std::string& outDir = "videos/");
    void record(int seconds = 10);        // simple blocking call
private:
    std::string outDir_;
};

WebcamRecorder::WebcamRecorder(const std::string& d) : outDir_(d) {}

void WebcamRecorder::record(int seconds) {
    cv::VideoCapture cap(0);
    if (!cap.isOpened()) throw std::runtime_error("no camera");

    int width  = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_WIDTH));
    int height = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_HEIGHT));
    auto fourcc = cv::VideoWriter::fourcc('m','p','4','v');
    std::string fname = outDir_ + "/capture_" +
                        std::to_string(std::time(nullptr)) + ".mp4";
    cv::VideoWriter writer(fname, fourcc, 20.0, {width, height});

    auto end = std::chrono::steady_clock::now() + std::chrono::seconds(seconds);
    cv::Mat frame;
    while (std::chrono::steady_clock::now() < end && cap.read(frame)) {
        writer.write(frame);
    }
}
