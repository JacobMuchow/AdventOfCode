#include "part2.h"

using namespace std;

void Day21Part2::loadShop(std::string inputFile) {
    weapons.push_back(make_shared<Item>("Dagger",       8,  4, 0));
    weapons.push_back(make_shared<Item>("Shortsword",   10, 5, 0));
    weapons.push_back(make_shared<Item>("Warhammer",    25, 6, 0));
    weapons.push_back(make_shared<Item>("Longsword",    40, 7, 0));
    weapons.push_back(make_shared<Item>("Greataxe",     74, 8, 0));

    armors.push_back(make_shared<Item>("None",       0,   0, 0));
    armors.push_back(make_shared<Item>("Leather",    13,  0, 1));
    armors.push_back(make_shared<Item>("Chainmail",  31,  0, 2));
    armors.push_back(make_shared<Item>("Splintmail", 53,  0, 3));
    armors.push_back(make_shared<Item>("Bandedmail", 75,  0, 4));
    armors.push_back(make_shared<Item>("Platemail",  102, 0, 5));

    rings.push_back(make_shared<Item>("None",        0,   0, 0));
    rings.push_back(make_shared<Item>("None",        0,   0, 0));
    rings.push_back(make_shared<Item>("Defense +1",  20,  0, 1));
    rings.push_back(make_shared<Item>("Damage +1",   25,  1, 0));
    rings.push_back(make_shared<Item>("Defense +2",  40,  0, 2));
    rings.push_back(make_shared<Item>("Damage +2",   50,  2, 0));
    rings.push_back(make_shared<Item>("Defense +3",  80,  0, 3));
    rings.push_back(make_shared<Item>("Damage +3",   100, 3, 0));
}

bool Day21Part2::simulate(std::shared_ptr<Loadout> myLoadout, int myHp, std::shared_ptr<Loadout> bossLoadout, int bossHp) {
    double myAttack = max(myLoadout->totalDamage - bossLoadout->totalArmor, 1); // 3
    double bossAttack = max(bossLoadout->totalDamage - myLoadout->totalArmor, 1); // 2

    double winTurn = ceil(bossHp / myAttack);
    int finalHealth = myHp - bossAttack * (winTurn-1);
    bool victory = finalHealth > 0;

    return victory;
}

// PT 2 NOTE: pretty easy change, we just need to sort highest -> lowest and check for first loss.
void Day21Part2::run(std::string inputFile) {
    this->loadShop("day21/shop.txt");

    // Build list of all possible loadouts
    for (auto& weapon : weapons) {
        for (auto& armor : armors) {

            for (size_t i = 0; i < rings.size(); i++) {
                auto& ring1 = rings[i];
                for (size_t j = i+1; j < rings.size(); j++) {
                    auto& ring2 = rings[j];

                    int totalCost = weapon->cost + armor->cost + ring1->cost + ring2->cost;
                    int totalDamage = weapon->damage + armor->damage + ring1->damage + ring2->damage;
                    int totalArmor = weapon->armor + armor->armor + ring1->armor + ring2->armor;

                    loadouts.push_back(make_shared<Loadout>(weapon, armor, ring1, ring2, totalCost, totalDamage, totalArmor));
                }
            }
        }
    }

    // Sort loadouts by cost - this is less efficient in terms of Big O, but
    // if our "simulation" function becomes more complex then this might be
    // helpful later as we can loop and exit on the first loadout giving victory.
    std::sort(loadouts.begin(), loadouts.end(), [](auto& l1, auto& l2) {
        return l1->totalCost > l2->totalCost;
    });

    // Go through loadouts from lowest -> highest cost until we beat the boss and exit.
    int myHp = 100;
    int bossHp = 104;
    auto bossLoadout = make_shared<Loadout>(nullptr, nullptr, nullptr, nullptr, 0, 8, 1);

    for (size_t i = 0; i < loadouts.size(); i++) {
        auto loadout = loadouts[i];

        if (!simulate(loadout, myHp, bossLoadout, bossHp)) {
            cout << "Defeat!" << endl;
            cout << "Loadout: ver - " << i << ", cost - " << loadout->totalCost << endl;
            return;
        }
    }

    cout << "No solution found... something went wrong D:" << endl;
}
