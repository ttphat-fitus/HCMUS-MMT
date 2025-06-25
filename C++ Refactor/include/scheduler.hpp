// Scheduler.hpp (very small)
#pragma once
#include <functional>
void schedule_every(std::chrono::seconds period, std::function<void()> job);
