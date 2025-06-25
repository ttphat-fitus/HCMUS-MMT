// Scheduler.cpp
#include "scheduler.hpp"
#include <thread>

void schedule_every(std::chrono::seconds period, std::function<void()> job) {
    std::thread([=] {
        while (true) { job(); std::this_thread::sleep_for(period); }
    }).detach();
}
