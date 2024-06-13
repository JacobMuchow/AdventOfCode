#include "part2.h"

using namespace std;

// Out of all my solutions so far, I am most displeased with this one.
// It's a pretty brute force & ugly way to solve the problem, and prone
// to errors, as I had one word with 4 repeated characters that should
// be considered NICE but my original solve was getting this wrong.
// I racked my brain on this problem for a while re-reading the fine print
// closely over and over. Eventually I caved and found some helpful grep/regex
// solutions that revealed to me the word I was not getting right. Which was
// a bit frustrating - I feel it's a detail I should have caught. And after
// tweaking the code to fix, the final solution feels really brittle.
bool isNice(string word) {
    unordered_map<string, bool> seenPairs = {};
    bool pairSeenTwice = false;
    bool sandwichSeen = false;

    for (int i = 1; i < word.length(); i++) {
        char c = word[i];

        // Check if this pair has been seen and set our flag if so.
        string key = string(1, (word[i-1])) + c;

        if (i > 1) {
            bool skip = false;

            // This is trying to avoid counting overlaps, but also make sure
            // if we get 4 characters in a row, that that still counts.
            if (c == word[i-1] && c == word[i-2]) {
                if (i < 3 || c != word[i-3]) {
                    skip = true;
                }
            }

            if (!skip && seenPairs.find(key) != seenPairs.end()) {
                pairSeenTwice = true;
            }
        }

        seenPairs[key] = true;

        // Check if a sandwich has been seen and set our flag if so.
        if (i > 1 && c == word[i-2]) {
            sandwichSeen = true;
        }
    }

    return pairSeenTwice && sandwichSeen;
}

void Day05Part2::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    int niceWords = 0;

    for (string line : lines) {
        bool nice = isNice(line);

        cout << line << " is " << (nice ? "nice" : "naughty") << endl;

        if (nice) {
            niceWords++;
        }
    }

    cout << "Nice word count: " << niceWords << endl;
}
