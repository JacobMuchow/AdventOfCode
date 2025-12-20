package solutions;

import utils.ResourceUtils;
import utils.Runnable;

import java.util.ArrayList;
import java.util.List;

public class Day09Pt1Solution implements Runnable {
    @Override
    public void run() {
        final var lines = ResourceUtils.readLines("resources/day09/input.txt");
        final List<Pos2d> points = this.parseInput(lines);

        long maxLen = 0;
        Pos2d maxP1 = null;
        Pos2d maxP2 = null;

        for (int i = 0; i < points.size() - 1; i++) {
            final var p1 = points.get(i);
            for (int j = i+1; j < points.size(); j++) {
                final var p2 = points.get(j);
                final var len = Math.abs(p2.x-p1.x) + Math.abs(p2.y-p1.y);
                if (len > maxLen) {
                    maxLen = len;
                    maxP1 = p1;
                    maxP2 = p2;
                }
            }
        }

        final var w = Math.abs(maxP2.x - maxP1.x) + 1;
        final var h = Math.abs(maxP2.y - maxP1.y) + 1;
        final var maxArea = w * h;
        System.out.printf("Max Area: %d\n", maxArea);
    }

    private List<Pos2d> parseInput(List<String> lines) {
        var points = new ArrayList<Pos2d>(lines.size());
        for (var line : lines) {
            var tokens = line.split(",");
            points.add(new Pos2d(
                Long.parseLong(tokens[0]),
                Long.parseLong(tokens[1])
            ));
        }
        return points;
    }

    record Pos2d(long x, long y) {}
}

