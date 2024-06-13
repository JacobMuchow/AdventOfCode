#include "part2.h"

using namespace std;

void Day25Part2::run(std::string inputFile) {
    cout << "Day 25" << endl;

    // Goal: Enter the code at row 3010, column 3019.
    
    // See notes in test.txt for how I came to this solution.

    auto computeCodeNum = [](auto row, auto col) {
        long long n = row+col-1;
        return n*(n+1)/2 - (row-1);
    };

    long long codeNum = computeCodeNum(3010, 3019);
    cout << "3010x3019:" << codeNum << endl;

    long long code = 20151125; // code 1

    // I thought doing this up to 18M iterations would be inefficient, but it's almost instant.
    for (int i = 1; i < codeNum; i++) {
        code = (code * 252533LL) % 33554393LL;
    }

    cout << "Code val: " << code << endl;
}
