#pragma once

#include "../runner.h"

#include <sstream>

enum ItemType {
    Weapon,
    Armor,
    Ring
};

struct Item {
    std::string name;
    int cost;
    int damage;
    int armor;

    Item(std::string name, int cost, int damage, int armor) {
        this->name = name;
        this->cost = cost;
        this->damage = damage;
        this->armor = armor;
    }

    std::string toString() {
        std::stringstream ss;
        ss << name << ": " << cost << " " << damage << " " << armor;
        return ss.str();
    }

    void print() {
        std::cout << toString() << std::endl;
    }
};

struct Loadout {
    std::shared_ptr<Item> weapon;
    std::shared_ptr<Item> armor;
    std::shared_ptr<Item> ring1;
    std::shared_ptr<Item> ring2;
    int totalCost;
    int totalDamage;
    int totalArmor;

    Loadout(std::shared_ptr<Item> weapon, std::shared_ptr<Item> armor, std::shared_ptr<Item> ring1, std::shared_ptr<Item> ring2,
            int totalCost, int totalDamage, int totalArmor) {
        this->weapon = weapon;
        this->armor = armor;
        this->ring1 = ring1;
        this->ring2 = ring2;
        this->totalCost = totalCost;
        this->totalDamage = totalDamage;
        this->totalArmor = totalArmor;
    }
};

class Day21Part2 : Runner {
private:
    std::vector<std::shared_ptr<Item>> weapons;
    std::vector<std::shared_ptr<Item>> armors;
    std::vector<std::shared_ptr<Item>> rings;

    std::vector<std::shared_ptr<Loadout>> loadouts;

private:
    void loadShop(std::string inputFile);
    bool simulate(std::shared_ptr<Loadout> myLoadout, int myHp, std::shared_ptr<Loadout> bossLoadout, int bossHp);

public:
    virtual void run(std::string inputFile);
};
