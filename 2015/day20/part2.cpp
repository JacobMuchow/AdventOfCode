#include "part2.h"

#include <regex>
#include <set>

using namespace std;

vector<int> Day20Part2::computeFactors(int number) {
    vector<int> rootFactors = {};
    vector<int> factors = {};

    double root = sqrt(number);

    int l = ceil(number/50.0);
    int u = ceil(root);

    for (int i = 1; i < u; i++) {
        if (number % i == 0) {
            rootFactors.push_back(i);
        }
    }

    for (int i : rootFactors) {
        if (i >= l) {
            factors.push_back(i);
        }
    }

    if (floor(root) == root && root >= l) {
        factors.push_back(root);
    }

    for (auto it = rootFactors.rbegin(); it != rootFactors.rend(); it++) {
        int factor = number / *it;
        if (factor >= l) {
            factors.push_back(number / *it);
        }
    }

    return factors;
}

int Day20Part2::sumFactors(int num) {
    vector<int> factors = computeFactors(num);

    int sum = 0;
    for (int i : factors) {
        sum += i;
    }
    return sum * 11;
}

int Day20Part2::findLower(int goal) {
    int total = 0;
    int i = 1;

    while (total < goal) {
        total += i++;
    }

    return i;
}

int Day20Part2::findUpper(int goal, int lower) {
    int num = lower;
    while (true) {
        int sum = sumFactors(num);
        cout << num << " -> " << sum << endl;
        if (sum >= goal) {
            break;
        }
        num += 10000;
    }

    return num;
}

int Day20Part2::searchLowest(int lower, int upper, int goal, int precision) {
    int dec = pow(10, precision);
    int soln = upper;

    for (int i = upper; i >= lower; i -= dec) {
        int sum = sumFactors(i);

        if (i % 10000 == 0) {
            cout << "Sum of " << i << " = " << sum << endl;
        }

        if (sum >= goal) {
            soln = i;
        }
    }

    return soln;
}

void Day20Part2::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    int goal = stoi(lines[0]);
    int lower = 831600;
    int upper = findUpper(goal, lower);

    cout << "Goal: " << goal << endl;
    cout << "Lower: " << lower << endl;
    cout << "Upper: " << upper << endl;


    int soln = upper;
    for (int prec = 6; prec >= 0; prec--) {
        soln = searchLowest(lower, soln, goal, prec);
    }

    cout << "\nSolution: " << soln << endl;
}
