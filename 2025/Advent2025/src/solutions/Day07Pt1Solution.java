package solutions;

import utils.ResourceUtils;
import utils.Runnable;

import java.util.HashSet;
import java.util.Set;

public class Day07Pt1Solution implements Runnable {
    @Override
    public void run() {
        final var grid = ResourceUtils.readCharGrid("resources/day07/input.txt");

        int start = findStartX(grid[0]);
        System.out.printf("start x: %d\n", start);

        var tachyonBeams = new HashSet<Integer>();
        tachyonBeams.add(start);

        var splitCount = 0;
        for (var y = 2; y < grid.length; y += 2) {
            var newBeams = new HashSet<Integer>();
            for (var beam : tachyonBeams) {
                if (grid[y][beam] == '^') {
                    newBeams.add(beam-1);
                    newBeams.add(beam+1);
                    splitCount += 1;
                } else {
                    newBeams.add(beam);
                }
            }
            tachyonBeams = newBeams;
        }

        System.out.printf("Split count: %d\n", splitCount);
    }

    private int findStartX(char[] topRow) {
        for (var i = 0; i < topRow.length; i++) {
            if (topRow[i] == 'S') return i;
        }
        throw new Error("Starting position not found");
    }
}

