#include "part1.h"

#include <regex>
#include <queue>

#include "../elements/utils.h"

using namespace std;

void Day07Part1::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);
    string line = lines[0];

    this->valueMap = {};
    this->solveQueue = {};

    for (string line : lines) {
        smatch sm;

        // Basic input
        if (regex_match(line, sm, regex("^([a-z|0-9]+) -> ([a-z]+)"))) {
            cout << "match: " << sm[1] << " -> " << sm[2] << endl;

            addToValueMapIfNumerical(sm[1]);
            solveQueue.push(make_shared<Connection>(sm[1], sm[2]));
            continue;
        }

        // NOT match
        if (regex_match(line, sm, regex("^NOT ([a-z|0-9]+) -> ([a-z]+)"))) {
            cout << "match: NOT " << sm[1] << " -> " << sm[2] << endl;

            addToValueMapIfNumerical(sm[1]);
            solveQueue.push(make_shared<NOTGate>(sm[1], sm[2]));
            continue;
        }

        // AND match
        if (regex_match(line, sm, regex("^([a-z|0-9]+) AND ([a-z|0-9]+) -> ([a-z]+)"))) {
            cout << "match: " << sm[1] << " AND " << sm[2] <<  " -> " << sm[3] << endl;

            addToValueMapIfNumerical(sm[1]);
            addToValueMapIfNumerical(sm[2]);
            solveQueue.push(make_shared<ANDGate>(sm[1], sm[2], sm[3]));
            continue;
        }

        // OR match
        if (regex_match(line, sm, regex("^([a-z|0-9]+) OR ([a-z|0-9]+) -> ([a-z]+)"))) {
            cout << "match: " << sm[1] << " OR " << sm[2] <<  " -> " << sm[3] << endl;

            addToValueMapIfNumerical(sm[1]);
            addToValueMapIfNumerical(sm[2]);
            solveQueue.push(make_shared<ORGate>(sm[1], sm[2], sm[3]));
            continue;
        }

        // LSHIFT match
        if (regex_match(line, sm, regex("^([a-z|0-9]+) LSHIFT ([0-9]+) -> ([a-z]+)"))) {
            cout << "match: " << sm[1] << " LSHIFT " << stoi(sm[2]) <<  " -> " << sm[3] << endl;

            addToValueMapIfNumerical(sm[1]);
            solveQueue.push(make_shared<LSHIFTGate>(sm[1], stoi(sm[2]), sm[3]));
            continue;
        }

        // RSHIFT match
        if (regex_match(line, sm, regex("^([a-z|0-9]+) RSHIFT ([0-9]+) -> ([a-z]+)"))) {
            cout << "match: " << sm[1] << " RSHIFT " << stoi(sm[2]) <<  " -> " << sm[3] << endl;

            addToValueMapIfNumerical(sm[1]);
            solveQueue.push(make_shared<RSHIFTGate>(sm[1], stoi(sm[2]), sm[3]));
            continue;
        }

        throw invalid_argument("Failed to parse line form instructions: " + line);
    }

    cout << "Executing solve queue...\n\n";

    while (!solveQueue.empty()) {
        shared_ptr<Component> c = solveQueue.front();
        solveQueue.pop();

        if (c->type() == "BASIC") {
            auto conn = dynamic_pointer_cast<Connection>(c);
            if (valueMap.find(conn->in) != valueMap.end()) {
                valueMap[conn->out] = valueMap[conn->in];
                continue;
            }
            solveQueue.push(c);
        }

        else if (c->type() == "NOT") {
            auto gate = dynamic_pointer_cast<NOTGate>(c);
            if (valueMap.find(gate->in) != valueMap.end()) {
                valueMap[gate->out] = ~valueMap[gate->in];
                continue;
            }
            solveQueue.push(c);
        }

        else if (c->type() == "AND") {
            auto gate = dynamic_pointer_cast<ANDGate>(c);
            if (valueMap.find(gate->in1) != valueMap.end() && valueMap.find(gate->in2) != valueMap.end()) {
                valueMap[gate->out] = valueMap[gate->in1] & valueMap[gate->in2];
                continue;
            }
            solveQueue.push(c);
        }

        else if (c->type() == "OR") {
            auto gate = dynamic_pointer_cast<ORGate>(c);
            if (valueMap.find(gate->in1) != valueMap.end() && valueMap.find(gate->in2) != valueMap.end()) {
                valueMap[gate->out] = valueMap[gate->in1] | valueMap[gate->in2];
                continue;
            }
            solveQueue.push(c);
        }

        else if (c->type() == "LSHIFT") {
            auto gate = dynamic_pointer_cast<LSHIFTGate>(c);
            if (valueMap.find(gate->in) != valueMap.end()) {
                valueMap[gate->out] = valueMap[gate->in] << gate->val;
                continue;
            }
            solveQueue.push(c);
        }

        else if (c->type() == "RSHIFT") {
            auto gate = dynamic_pointer_cast<RSHIFTGate>(c);
            if (valueMap.find(gate->in) != valueMap.end()) {
                valueMap[gate->out] = valueMap[gate->in] >> gate->val;
                continue;
            }
            solveQueue.push(c);
        }

        else {
            throw invalid_argument("Unknown component type in queue: " + c->type());
        }
    }

    cout << "Value map:\n";
    for (auto entry : valueMap) {
        cout << entry.first << ": " << entry.second << endl;
    }

    cout << "\nsignal to a: " << valueMap["a"] << endl;
}

bool Day07Part1::addToValueMapIfNumerical(std::string name) {
    if (!Utils::isNumerical(name)) return false;

    valueMap[name] = ushort(stoi(name));
    return true;
}
