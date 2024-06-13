#pragma once

#include <iostream>
#include <fstream>
#include <vector>
#include <regex>

#include <nlohmann/json.hpp>
using json = nlohmann::json;

class Runner
{
protected:
    std::vector<std::string> readLinesFromFile(std::string inputFile);
    json readJsonFromFile(std::string inputFile);

    std::vector<std::string> split(std::string s, std::string delimiter);

public:
    virtual void run(std::string inputFile) = 0;
};
