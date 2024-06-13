#pragma once

#include <string>
#include <regex>

class Utils {
public:
    static bool isNumerical(std::string s) {
        return std::regex_match(s, std::regex("[0-9]+"));
    }
};
