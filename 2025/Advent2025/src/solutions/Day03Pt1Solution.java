package solutions;

import utils.ResourceUtils;
import utils.Runnable;

public class Day03Pt1Solution implements Runnable {
    @Override
    public void run() {
        var lines = ResourceUtils.readLines("resources/day03/input.txt");

        var maxJoltage = 0;

        for (var line : lines) {
            var max1 = -1;
            var maxI = -1;
            var max2 = -1;

            for (var i = 0; i < line.length()-1; i++) {
                var joltage = Integer.parseInt(line.substring(i, i+1));
                if (joltage > max1) {
                    max1 = joltage;
                    maxI = i;
                }
            }

            for (var i = maxI + 1; i < line.length(); i++) {
                var joltage = Integer.parseInt(line.substring(i, i+1));
                if (joltage > max2) {
                    max2 = joltage;
                }
            }

            maxJoltage += 10 * max1 + max2;
        }

        System.out.printf("Max joltage: %d\n", maxJoltage);
    }
}
