#include "part1.h"

#include <sstream>

using namespace std;

void Day11Part1::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    string line = lines[0];
    cout << line << endl;

    string next = nextPassword(line);
    cout << "next pass: " << next << endl;
}

string Day11Part1::nextPassword(string password) {
    string newPass(password);

    // First, correct any illegal characters
    bool corrected = false;
    for (int i = 0; i < newPass.length(); i++) {
        if (invalidChar(newPass[i])) {
            newPass = incrementAt(newPass, i);
            corrected = true;
            break;
        }
    }

    // The corrected password suffices.
    if (corrected && passwordValid(newPass) == 0) {
        return newPass;
    }

    do {
        int j = newPass.length()-1;
        while (j > 0 && newPass[j] == 'z') {
            j--;
        }

        newPass = incrementAt(newPass, j);

    } while (passwordValid(newPass) < 0);

    return newPass;
}

std::string Day11Part1::incrementAt(std::string pass, int pos) {
    if (pass[pos] == 'z') {
        throw invalid_argument("incrementAt() should not have been called with arg z");
    }

    // Increment at pos and set all succeeding to 'a'.
    pass[pos] += 1;
    if (invalidChar(pass[pos])) {
        pass[pos] += 1;
    }

    for (int j = pos+1; j < pass.length(); j++) {
        pass[j] = 'a';
    }

    return pass;
}

int Day11Part1::passwordValid(std::string str) {
    // Rule 2 - invalid if it contains i,l,o
    for (int i = 0; i < str.length(); i++) {
        if (invalidChar(str[i])) return -2;
    }

    // Rule 1 - Requires >= 1 "straight" (ex. abc, def, xyz).
    bool hasStraight = false;
    for (int i = 0; i < str.length()-2; i++) {
        if (str[i+1] == str[i]+1) {
            i++;
            if (str[i+1] == str[i]+1) {
                hasStraight = true;
                break;
            }
        }
    }

    if (!hasStraight) return -1;

    // Rule 3 - Requires >= 2 pairs (avoid overlaps).
    int numPairs = 0;

    for (int i = 0; i < str.length()-1; i++) {
        if (str[i] == str[i+1]) {
            if (++numPairs == 2) return 0;
            i++;
        }
    }

    return -3;
}

bool Day11Part1::invalidChar(char val) {
    return val == 'i' || val == 'l' || val == 'o';
}
