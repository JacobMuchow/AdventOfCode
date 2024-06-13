#include "part1.h"

#include "../elements/md5.h"

using namespace std;

void Day04Part1::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    // Only 1 line for this one.
    string key = lines[0];
    long long num = 1;

    while(true) {
        if (num % 10000 == 0) {
            cout << num << endl;
        }

        string hashKey = key + to_string(num);
        string hash = md5(hashKey);

        if (
            hash[0] == '0' &&
            hash[1] == '0' &&
            hash[2] == '0' &&
            hash[3] == '0' &&
            hash[4] == '0'
        ) {
            break;
        }

        num++;
    }

    cout << "special num: " << num << endl;
}
