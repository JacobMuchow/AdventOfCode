#include "part1.h"

#include <regex>
#include <set>

using namespace std;

long long Day15Part1::getScore(vector<int> dist) {
    long long cScore = 0;
    long long tScore = 0;
    long long fScore = 0;
    long long dScore = 0;

    for (int i = 0; i < dist.size(); i++) {
        auto& ing = ingredients[i];

        cScore += ing->capacity * dist[i];
        tScore += ing->texture * dist[i];
        fScore += ing->flavor * dist[i];
        dScore += ing->durability * dist[i];
    }

    if (cScore <= 0 || tScore <= 0 || fScore <= 0 || dScore <= 0) {
        return 0;
    }

    return cScore * tScore * fScore * dScore;
}

/**
 * This is a brute force solution to calculate best score by testing all permutations of
 * teaspoon distribution. If you look at other solutions, many peole simply wrote 4 for loops to brute force,
 * but since the example has 2 ingredients instead of 5, I wanted to make some more robust / generic,
 * so I cooked up this solution that recursively builds for loops. Kind of happy with it, though I feel
 * like there must be some better way of doing this than pure brute force. Like striding distrubtions, binary
 * search... there are probably some large ranges where scores are all 0 or nowhere close to best that could
 * logically be jumped over. But alas.
 */
long long Day15Part1::findBestScoreRecursive(vector<int> dist, int idx, int tspAvailable, long long bestScore) {
    if (idx == dist.size()-1) {
        dist[idx] = tspAvailable;
        return max(bestScore, getScore(dist));
    }

    int recursiveDepthRemaining = dist.size() - idx - 1;

    for (int i = 1; i <= tspAvailable - recursiveDepthRemaining; i++) {
        dist[idx] = i;
        bestScore = findBestScoreRecursive(dist, idx+1, tspAvailable-i, bestScore);
    }

    return bestScore;
}

void Day15Part1::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    for (string& line : lines) {
        smatch sm;
        bool hasMatch = regex_match(line, sm, regex("^(.*): capacity (.*), durability (.*), flavor (.*), texture (.*), calories (.*)"));
        if (!hasMatch) {
            throw invalid_argument("Error parsing line from input: " + line);
        }

        auto ingredient = make_shared<Ingredient>(
            sm[1],
            stoi(sm[2]),
            stoi(sm[3]),
            stoi(sm[4]),
            stoi(sm[5]),
            stoi(sm[6])
        );

        cout << ingredient->name << ": " << ingredient->capacity << ", " << ingredient->durability << ", " << ingredient->flavor << ", " << ingredient->texture << ", " << ingredient->calories << endl;
        ingredients.push_back(ingredient);
    }

    vector<int> dist(ingredients.size(), 0);

    auto bestScore = findBestScoreRecursive(dist, 0, 100, 0);
    cout << "Best score found: " << bestScore << endl;
}
