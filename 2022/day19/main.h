#pragma once
#include <stdio.h>

struct Cost
{
    uint32_t ore;
    uint32_t clay;
    uint32_t obsidian;
};

struct Blueprint
{
    uint32_t id;
    struct Cost ore_robot_cost;
    struct Cost clay_robot_cost;
    struct Cost obsidian_robot_cost;
    struct Cost geode_robot_cost;
    uint32_t best; // Store the best result here.
};