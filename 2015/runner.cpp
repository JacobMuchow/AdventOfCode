#include "runner.h"

using namespace std;

vector<string> Runner::readLinesFromFile(string filePath) {
    ifstream file(filePath);
    if (!file.is_open()) {
        throw runtime_error("Unable to open file at: " + filePath);
    }

    // String to store each line of the file.
    string line;
    vector<string> lines;

    // Read each line from the file and store it in the
    // 'line' variable.
    while (getline(file, line)) {
        lines.push_back(line);
    }

    // Close the file stream once all lines have been
    // read.
    file.close();
    return lines;
}

json Runner::readJsonFromFile(string filePath) {
    ifstream file(filePath);
    if (!file.is_open()) {
        throw runtime_error("Unable to open file at: " + filePath);
    }

    return json::parse(file);
}

vector<string> Runner::split(string s, string delimiter) {
    size_t pos_start = 0, pos_end, delim_len = delimiter.length();
    string token;
    vector<string> res;

    while ((pos_end = s.find(delimiter, pos_start)) != string::npos) {
        token = s.substr(pos_start, pos_end - pos_start);
        pos_start = pos_end + delim_len;
        res.push_back(token);
    }

    res.push_back(s.substr (pos_start));
    return res;
}
