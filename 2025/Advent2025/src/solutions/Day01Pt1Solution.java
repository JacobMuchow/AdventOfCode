package solutions;

import utils.ResourceUtils;
import utils.Runnable;

import java.util.ArrayList;
import java.util.List;

public class Day01Pt1Solution implements Runnable {
    @Override
    public void run() {
        var lines = ResourceUtils.readLines("resources/day01/input.txt");

        var dirs = new ArrayList<String>();
        var counts = new ArrayList<Integer>();

        for (var line : lines) {
            dirs.add(line.substring(0, 1));
            counts.add(Integer.parseInt(line.substring(1)));
        }

        var zeroCount = 0;
        var dial = 50;

        for (var i = 0; i < dirs.size(); i++) {
            var dir = dirs.get(i);
            var ticks = counts.get(i) % 100;

            if (dir.equals("R")) {
                dial += ticks;
                if (dial > 99) {
                    dial -= 100;
                }
            } else {
                dial -= ticks;
                if (dial < 0) {
                    dial += 100;
                }
            }

            if (dial == 0) {
                zeroCount++;
            }
        }

        System.out.printf("Zero count: %d\n", zeroCount);
    }
}
