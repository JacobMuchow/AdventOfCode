#pragma once

#include "../runner.h"

enum GameCondition {
    Ongoing,
    Victory,
    Defeat
};

enum Spell {
    MagicMissle = 0,
    Drain,
    Shield,
    Poison,
    Recharge
};

struct Effect {
    int turnsLeft = 0;
};

struct PawnState {
    int hp;
    int armor;
    int damage;
    int mana;

    PawnState(int hp, int armor, int damage, int mana) {
        this->hp = hp;
        this->armor = armor;
        this->damage = damage;
        this->mana = mana;
    }
};

struct GameState {
    PawnState player;
    PawnState boss;
    int manaUsed = 0;

    // In an abstracted system, what might create a list or map of effects
    // per Pawn as a part of their state. Conveniently only one instance
    // of each spell can be active, so we can skirt around building a big
    // abstraction (hopefully pt 2 doesn't bite me).
    // turnsLeft = 0 when inactive.
    Effect shieldEffect = Effect { 0 };
    Effect poisonEffect = Effect { 0 };
    Effect rechargeEffect = Effect { 0 };

    GameState(PawnState player, PawnState boss) : player(player), boss(boss) {}
};

class Day22Part1 : Runner {
private:
    int spellCost(Spell spell);
    void printState(GameState state);
    GameCondition checkGameCondition(GameState state);
    GameState processEffects(GameState state);
    GameState playerAction(GameState state, Spell spell);
    GameState bossAction(GameState state);

    void testScenario(GameState state, std::vector<Spell> playerActions);
    int leastManaRecursive(GameState state, int leastMana);

public:
    virtual void run(std::string inputFile);
};
