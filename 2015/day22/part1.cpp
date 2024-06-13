#include "part1.h"

using namespace std;

#define DEBUG 0

int Day22Part1::spellCost(Spell spell) {
    switch (spell) {
    case MagicMissle: return 53;
    case Drain: return 73;
    case Shield: return 113;
    case Poison: return 173;
    case Recharge: return 229;
    }
}

void Day22Part1::printState(GameState state) {
    if (!DEBUG) return;
    cout << "- Player has " << state.player.hp << " hp, " << state.player.armor << " armor, " << state.player.mana << " mana" << endl;
    cout << "- Boss has " << state.boss.hp << " hp" << endl;
}

GameCondition Day22Part1::checkGameCondition(GameState state) {
    if (state.player.hp <= 0) return Defeat;
    if (state.boss.hp <= 0) return Victory;
    return Ongoing;
}

GameState Day22Part1::processEffects(GameState state) {
    // Shield
    if (state.shieldEffect.turnsLeft > 0) {
        state.shieldEffect.turnsLeft--;
        if(DEBUG) cout << "Shield's timer is now " << state.shieldEffect.turnsLeft << endl;

        if (state.shieldEffect.turnsLeft == 0) {
            state.player.armor = 0;
            if(DEBUG) cout << "Shield wears off, decreasing armor by 7" << endl;
        }
    }

    // Poison
    if (state.poisonEffect.turnsLeft > 0) {
        state.poisonEffect.turnsLeft--;
        state.boss.hp -= 3;
        if(DEBUG) cout << "Poison deals 3 damage; its timer is now " << state.poisonEffect.turnsLeft << endl;

        if (state.poisonEffect.turnsLeft == 0) {
            if(DEBUG) cout << "Poison wears off" << endl;
        }
    }

    // Recharge
    if (state.rechargeEffect.turnsLeft > 0) {
        state.rechargeEffect.turnsLeft--;
        state.player.mana += 101;
        if(DEBUG) cout << "Recharge provides 101 mana; its timer is now " << state.rechargeEffect.turnsLeft << endl;

        if (state.rechargeEffect.turnsLeft == 0) {
            if(DEBUG) cout << "Recharge wears off" << endl;
        }
    }

    return state;
}

GameState Day22Part1::playerAction(GameState state, Spell spell) {
    if(DEBUG) cout << "-- Player turn --" << endl;
    printState(state);
    state = processEffects(state);
    if (checkGameCondition(state) != Ongoing) {
        return state;
    }

    int cost = spellCost(spell);
    state.player.mana -= cost;
    state.manaUsed += cost;

    switch (spell) {
    case MagicMissle:
        if(DEBUG) cout << "Player casts Magic Missle, dealing 4 damage." << endl;
        state.boss.hp -= 4;
        break;

    case Drain:
        if(DEBUG) cout << "Player casts Drain, dealing 2 damage, and healing 2 hp." << endl;
        state.boss.hp -= 2;
        state.player.hp += 2;
        break;

    case Shield:
        if(DEBUG) cout << "Player casts Shield, increasing armor by 7." << endl;
        state.player.armor = 7;
        state.shieldEffect.turnsLeft = 6;
        break;

    case Poison:
        if(DEBUG) cout << "Player casts Poison." << endl;
        state.poisonEffect.turnsLeft = 6;
        break;

    case Recharge:
        if(DEBUG) cout << "Player casts Recharge." << endl;
        state.rechargeEffect.turnsLeft = 5;
        break;
    }

    if(DEBUG) cout << endl;
    return state;
}

GameState Day22Part1::bossAction(GameState state) {
    if(DEBUG) cout << "-- Boss turn --" << endl;
    printState(state);
    state = processEffects(state);
    if (checkGameCondition(state) != Ongoing) {
        return state;
    }

    int bossAttack = state.boss.damage - state.player.armor;
    if(DEBUG) cout << "Boss attacks for " << bossAttack << " damage!" << endl;

    state.player.hp -= bossAttack;

    if(DEBUG) cout << endl;
    return state;
}

void Day22Part1::testScenario(GameState gameState, std::vector<Spell> playerActions) {
    GameCondition gameCondition = Ongoing;

    for (auto& spell : playerActions) {
        // Player turn
        gameState = playerAction(gameState, spell);
        gameCondition = checkGameCondition(gameState);
        if (gameCondition != Ongoing) {
            break;
        }

        // Boss turn
        gameState = bossAction(gameState);
        gameCondition = checkGameCondition(gameState);
        if (gameCondition != Ongoing) {
            break;
        }
    }

    cout << "Sim complete." << endl;
    switch (gameCondition) {
    case Victory: cout << "Victory!" << endl; break;
    case Defeat: cout << "Defeat." << endl; break;
    case Ongoing: cout << "No victor." << endl; break;
    }
}

int Day22Part1::leastManaRecursive(GameState curState, int leastMana) {
    vector<Spell> spellList = { Recharge, Shield, Drain, Poison, MagicMissle };
    GameCondition gameCondition = Ongoing;

    for (auto& spell : spellList) {
        // Skip spells that cannot be used
        if (curState.player.mana < spellCost(spell)) {
            continue;
        }

        if (spell == Shield && curState.shieldEffect.turnsLeft > 0) continue;
        if (spell == Poison && curState.poisonEffect.turnsLeft > 0) continue;
        if (spell == Recharge && curState.rechargeEffect.turnsLeft > 0) continue;

        // Player turn
        GameState newState = playerAction(curState, spell);
        gameCondition = checkGameCondition(newState);
        if (gameCondition == Defeat) {
            continue;
        } else if (gameCondition == Victory) {
            leastMana = min(leastMana, newState.manaUsed);
        } else if (newState.manaUsed >= leastMana) {
            continue;
        }

        // Boss turn
        newState = bossAction(newState);
        gameCondition = checkGameCondition(newState);
        if (gameCondition == Defeat) {
            continue;
        } else if (gameCondition == Victory) {
            leastMana = min(leastMana, newState.manaUsed);
        } else {
            leastMana = leastManaRecursive(newState, leastMana);
        }
    }

    return leastMana;
}

void Day22Part1::run(std::string inputFile) {
    // Test 1
//    PawnState player = PawnState(10, 0, 0, 250);
//    PawnState boss = PawnState(13, 0, 8, 0);
//    GameState gameState = GameState(player, boss);

//    testScenario(gameState, { Poison, MagicMissle });

    // Test 2
//    PawnState player = PawnState(10, 0, 0, 250);
//    PawnState boss = PawnState(14, 0, 8, 0);
//    GameState gameState = GameState(player, boss);

//    testScenario(gameState, { Recharge, Shield, Drain, Poison, MagicMissle });

    // Puzzle
    PawnState player = PawnState(50, 0, 0, 500);
    PawnState boss = PawnState(55, 0, 8, 0);

    GameState gameState = GameState(player, boss);

    int leastMana = leastManaRecursive(gameState, INT_MAX);
    cout << "Least mana possible: " << leastMana << endl;
}
