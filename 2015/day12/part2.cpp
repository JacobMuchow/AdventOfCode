#include "part2.h"

#include <regex>

using namespace std;

void Day12Part2::run(std::string inputFile) {
    json jsonFile = readJsonFromFile(inputFile);

    int total = totalRecursive(jsonFile);
    cout << "Total: " << total << endl;
}

int Day12Part2::totalRecursive(json jsonObj) {
    if (jsonObj.is_array()) {
        int total = 0;
        for (auto it = jsonObj.begin(); it != jsonObj.end(); it++) {
            total += totalRecursive(*it);
        }
        return total;
    } else if (jsonObj.is_object()) {
        // Ignore obj if it has "red" as any value.
        // Checking this before doing recursive walk is more optimal.
        for (auto it = jsonObj.begin(); it != jsonObj.end(); it++) {
            if (it->is_string() && it.value() == "red") {
                return 0;
            }
        }

        // Get recursive totals.
        int total = 0;
        for (auto it = jsonObj.begin(); it != jsonObj.end(); it++) {
            total += totalRecursive(it.value());
        }
        return total;
    } else if (jsonObj.is_number()) {
        int value;
        return jsonObj.get<int>();
    }

    return 0;
}
