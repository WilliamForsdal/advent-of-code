// Had to sudo apt install gdb for debugging to work in wsl.
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#include "main.h"

#include "data.c"
int test_bp(struct Blueprint *bp);
bool can_build(struct Cost *stock, struct Cost *robot_cost);
struct Cost cost_subtract(struct Cost *a, struct Cost *b);

int main()
{
    int i;
    for (i = 0; i < NUM_BPS; i++)
    {
        test_bp(&bps[i]);
        printf("Made %d geodes with bp %d\n", bps[i].best, i + 1);
    }
}

int test_bp(struct Blueprint *bp)
{
    int ore_robots = 1;
    int clay_robots = 0;
    int obsidian_robots = 0;
    int geode_robots = 0;
    struct Cost stock = {0};
    
    int obs_per_geode_robot = bp->geode_robot_cost.obsidian;

    int minute;
    for (minute = 1; minute <= 24; minute += 1)
    {
        int robot_built = 0;
        // if (can_build(&stock, &bp->geode_robot_cost))
        // {
        //     robot_built = 4;
        //     stock = cost_subtract(&stock, &bp->geode_robot_cost);
        // }
        // else if (can_build(&stock, &bp->obsidian_robot_cost))
        // {
        //     robot_built = 3;
        //     stock = cost_subtract(&stock, &bp->obsidian_robot_cost);
        // }
        // else if (can_build(&stock, &bp->clay_robot_cost))
        // {
        //     robot_built = 2;
        //     stock = cost_subtract(&stock, &bp->clay_robot_cost);
        // }
        // else if (can_build(&stock, &bp->ore_robot_cost))
        // {
        //     robot_built = 1;
        //     stock = cost_subtract(&stock, &bp->ore_robot_cost);
        // }

        // Collect ore
        stock.ore += ore_robots;
        stock.clay += clay_robots;
        stock.obsidian += obsidian_robots;
        bp->best += geode_robots;

        // robots completed.
        if (robot_built == 1)
        {
            ore_robots += 1;
        }
        else if (robot_built == 2)
        {
            clay_robots += 1;
        }
        else if (robot_built == 3)
        {
            obsidian_robots += 1;
        }
        else if (robot_built == 4)
        {
            geode_robots += 1;
        }
    }
}

bool can_build(struct Cost *stock, struct Cost *robot_cost)
{
    return stock->ore >= robot_cost->ore && stock->clay >= robot_cost->clay && stock->obsidian >= robot_cost->obsidian;
}
struct Cost cost_subtract(struct Cost *a, struct Cost *b)
{
    struct Cost result = {.ore = a->ore, .clay = a->clay, .obsidian = a->obsidian};
    result.ore -= b->ore;
    result.clay -= b->clay;
    result.obsidian -= b->obsidian;
    return result;
}