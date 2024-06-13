#pragma once

#include "../runner.h"

#include <queue>

struct Component {
    virtual std::string type() const = 0;
    virtual std::string str() const = 0;
};

struct Connection : Component {
    std::string in;
    std::string out;

    Connection(std::string in, std::string out) {
        this->in = in;
        this->out = out;
    }

    std::string type() const { return "BASIC"; }
    std::string str() const { return "BASIC: " + in + " -> " + out; }
};

struct NOTGate : Component {
    std::string in;
    std::string out;

    NOTGate(std::string in, std::string out) {
        this->in = in;
        this->out = out;
    }

    std::string type() const { return "NOT"; }
    std::string str() const { return "NOT: " + in + " -> " + out; }
};

struct ANDGate : Component {
    std::string in1;
    std::string in2;
    std::string out;

    ANDGate(std::string in1, std::string in2, std::string out) {
        this->in1 = in1;
        this->in2 = in2;
        this->out = out;
    }

    std::string type() const { return "AND"; }
    std::string str() const { return "AND: " + in1 + "," + in2 + " -> " + out; }
};

struct ORGate : Component {
    std::string in1;
    std::string in2;
    std::string out;

    ORGate(std::string in1, std::string in2, std::string out) {
        this->in1 = in1;
        this->in2 = in2;
        this->out = out;
    }

    std::string type() const { return "OR"; }
    std::string str() const { return "OR: " + in1 + "," + in2 + " -> " + out; }
};

struct LSHIFTGate : Component {
    std::string in;
    ushort val;
    std::string out;

    LSHIFTGate(std::string in, ushort val, std::string out) {
        this->in = in;
        this->val = val;
        this->out = out;
    }

    std::string type() const { return "LSHIFT"; }
    std::string str() const { return "LSHIFT: " + in + " " + std::to_string(val) + " -> " + out; }
};

struct RSHIFTGate : Component {
    std::string in;
    ushort val;
    std::string out;

    RSHIFTGate(std::string in, ushort val, std::string out) {
        this->in = in;
        this->val = val;
        this->out = out;
    }

    std::string type() const { return "RSHIFT"; }
    std::string str() const { return "RSHIFT: " + in + " " + std::to_string(val) + " -> " + out; }
};

class Day07Part2 : Runner {
public:
    virtual void run(std::string inputFile);

private:
    bool addToValueMapIfNumerical(std::string name);
    ushort getValue(std::string name);

private:
    std::unordered_map<std::string, ushort> valueMap = {};
    std::queue<std::shared_ptr<Component>> solveQueue = {};
};
