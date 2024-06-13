#include "part2.h"

using namespace std;

void Day23Part2::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    unordered_map<string, uint> registers = {
        { "a", 1 },
        { "b", 0 }
    };

    for (size_t i = 0; i < lines.size();) {
        string line = lines[i];
        cout << line << endl;

        smatch sm;
        bool hasMatch = regex_match(line, sm, regex("^([a-z]+) (.*)$"));
        if (!hasMatch) {
            cout << "Error reading line" << endl;
            break;
        }

        string instruction = sm[1];
        string options = sm[2];

        if (instruction == "hlf") {
            registers[options] /= 2;
        } else if (instruction == "tpl") {
            registers[options] *= 3;
        } else if (instruction == "inc") {
            registers[options] += 1;
        } else if (instruction == "jmp") {
            int offset = stoi(options);
            i += offset;
            continue;

        } else if (instruction == "jie" || instruction == "jio") {
            hasMatch = regex_match(options, sm, regex("^([a-z]+), ([+-][0-9]+)$"));
            if (!hasMatch) {
                cout << "Failed to parse jump instructions from line. Exiting. Options: " << options << endl;
                break;
            }

            string reg = sm[1];
            int offset = stoi(sm[2]);

            // Jump if even
            if (instruction == "jie") {
                if (registers[reg] % 2 == 0) {
                    i += offset;
                    continue;
                }
            }

            // Jump if "one"
            else if (registers[reg] == 1) {
                i += offset;
                continue;
            }
        } else {
            cout << "Unkown instruction: " << instruction << ". Exiting." << endl;
            break;
        }

        i++;
    }

    cout << endl << "Program exited." << endl;
    cout << "Final values of registers:" << endl;
    cout << "a: " << registers["a"] << endl;
    cout << "b: " << registers["b"] << endl;
}
