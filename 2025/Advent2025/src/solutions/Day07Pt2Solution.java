package solutions;

import utils.ResourceUtils;
import utils.Runnable;

import java.util.HashMap;
import java.util.HashSet;

public class Day07Pt2Solution implements Runnable {
    public void run() {
        final var grid = ResourceUtils.readCharGrid("resources/day07/input.txt");

        int start = findStartX(grid[0]);
        System.out.printf("start x: %d\n", start);

        var tachyonBeams = new HashMap<Integer, Long>();
        tachyonBeams.put(start, 1L);

        for (var y = 2; y < grid.length; y += 2) {
            final var newBeams = new HashMap<Integer, Long>();
            for (var entry : tachyonBeams.entrySet()) {
                final var x = entry.getKey();
                final var timelines = entry.getValue();

                if (grid[y][x] == '^') {
                    long acc = newBeams.getOrDefault(x-1, 0L);
                    newBeams.put(x-1, acc+timelines);
                    acc = newBeams.getOrDefault(x+1, 0L);
                    newBeams.put(x+1, acc+timelines);
                } else {
                    newBeams.put(x, newBeams.getOrDefault(x, 0L) + timelines);
                }
            }
            tachyonBeams = newBeams;
        }

        long timelineCount = tachyonBeams.values().stream().reduce(0L, Long::sum);
        System.out.printf("Num timelines: %d\n", timelineCount);
    }

    private int findStartX(char[] topRow) {
        for (var i = 0; i < topRow.length; i++) {
            if (topRow[i] == 'S') return i;
        }
        throw new Error("Starting position not found");
    }
}

