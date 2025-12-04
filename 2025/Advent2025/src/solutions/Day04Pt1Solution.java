package solutions;

import utils.ResourceUtils;
import utils.Runnable;

import java.util.List;

public class Day04Pt1Solution implements Runnable {
    @Override
    public void run() {
        var lines = ResourceUtils.readLines("resources/day04/input.txt");
        char[][] grid = lines.stream().map(String::toCharArray).toArray(char[][]::new);

        var numAccessible = 0;

        for (var y = 0; y < grid.length; y++) {
            for (var x = 0; x < grid[y].length; x++) {
                if (grid[y][x] != '@') continue;
                if (isToiletPaperAccessible(grid, x, y)) {
                    numAccessible++;
                }
            }
        }

        System.out.printf("Num accessible: %d\n", numAccessible);
    }

    private boolean isToiletPaperAccessible(char[][] grid, int x, int y) {
        var neighborCount = 0;

        if (x > 0) {
            if (y > 0 && grid[y-1][x-1] == '@') neighborCount++;
            if (grid[y][x-1] == '@') neighborCount++;
            if (y < grid.length-1 && grid[y+1][x-1] == '@') neighborCount++;
        }

        if (y > 0 && grid[y-1][x] == '@') neighborCount++;
        // Skip self
        if (y < grid.length-1 && grid[y+1][x] == '@') neighborCount++;

        if (x < grid[0].length-1) {
            if (y > 0 && grid[y-1][x+1] == '@') neighborCount++;
            if (grid[y][x+1] == '@') neighborCount++;
            if (y < grid.length-1 && grid[y+1][x+1] == '@') neighborCount++;
        }

        return neighborCount < 4;
    }
}
