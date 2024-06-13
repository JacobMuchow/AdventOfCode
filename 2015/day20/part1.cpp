#include "part1.h"

#include <regex>
#include <set>

using namespace std;

vector<int> Day20Part1::computeFactors(int number) {
    vector<int> rootFactors = {};
    vector<int> factors = {};

    double root = sqrt(number);

    for (int i = 1; i < ceil(root); i++) {
        if (number % i == 0) {
            rootFactors.push_back(i);
        }
    }

    for (int i : rootFactors) {
        factors.push_back(i);
    }

    if (floor(root) == root) {
        factors.push_back(root);
    }

    for (auto it = rootFactors.rbegin(); it != rootFactors.rend(); it++) {
        factors.push_back(number / *it);
    }

    return factors;
}

int Day20Part1::sumFactors(int num) {
    vector<int> factors = computeFactors(num);

    int sum = 0;
    for (int i : factors) {
        sum += i;
    }
    return sum;
}

int Day20Part1::findLower(int goal) {
    int total = 0;
    int i = 1;

    while (total < goal) {
        total += i++;
    }

    return i;
}

int Day20Part1::findUpper(int goal) {
    int upper = goal;

    for (int num = upper; num > 0; num /= 2) {
        int sum = sumFactors(num);
        if (sum >= goal) {
            upper = num;
        }
    }

    return upper;
}

int Day20Part1::searchLowest(int lower, int upper, int goal, int precision) {
    int dec = pow(10, precision);
    int soln = upper;

    for (int i = upper; i >= lower; i -= dec) {
        int sum = sumFactors(i);

        if (i % 1000 == 0) {
            cout << "Sum of " << i << " = " << sum << endl;
        }

        if (sum >= goal) {
            soln = i;
        }
    }

    return soln;
}

void Day20Part1::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    int goal = stoi(lines[0]) / 10;
    int lower = findLower(goal);
    int upper = findUpper(goal);

    cout << "Goal: " << goal << endl;
    cout << "Lower: " << lower << endl;
    cout << "Upper: " << upper << endl;

    int soln = upper;
    for (int prec = 6; prec >= 0; prec--) {
        soln = searchLowest(lower, soln, goal, prec);
    }

    cout << "\nSolution: " << soln << endl;
}
