#pragma once

#include <ostream>
#include <sstream>

struct Pos2D {
    int x, y;

    std::string key() const {
        std::stringstream ss;
        ss << x << "," << y;
        return ss.str();
    }
};
