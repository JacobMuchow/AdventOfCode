package solutions;

import utils.ResourceUtils;
import utils.Runnable;

import java.util.ArrayList;
import java.util.List;

public class Day08Pt1Solution implements Runnable {
    @Override
    public void run() {
        final var lines = ResourceUtils.readLines("resources/day08/test.txt");
        final List<Vec3D> points = new ArrayList<>(lines.size());
        final var pairAmount = 10;

        for (var line : lines) {
            final var tokens = line.split(",");
            points.add(new Vec3D(
                Long.parseLong(tokens[0]),
                Long.parseLong(tokens[1]),
                Long.parseLong(tokens[2])
            ));
        }

        final List<Pairing> nearestPairs = new ArrayList<>(pairAmount);

        for (int i = 0; i < points.size()-1; i++) {
            final var p1 = points.get(i);
            for (int j = i+1; j < points.size(); j++) {
                var p2 = points.get(j);
                var dist = Math.sqrt(Math.powExact((p2.x-p1.x), 2) + Math.powExact((p2.y-p1.y), 2) + Math.powExact((p2.z-p1.z), 2));

                if (nearestPairs.size() < pairAmount) {
                    this.insertPair(nearestPairs, new Pairing(p1, p2, dist));
                } else {
                    final var lastPair = nearestPairs.getLast();
                    if (dist < lastPair.dist) {
                        nearestPairs.removeLast();
                        this.insertPair(nearestPairs, new Pairing(p1, p2, dist));
                    }
                }
            }
        }

        for (var pair : nearestPairs) {
            System.out.printf("%d,%d,%d - %d,%d,%d\n", pair.p1.x, pair.p1.y, pair.p1.z, pair.p2.x, pair.p2.y, pair.p2.z);
        }
    }

    private void insertPair(List<Pairing> pairs, Pairing newPair) {
        var insertIdx = -1;
        for (int i = 0; i < pairs.size(); i++) {
            if (newPair.dist < pairs.get(i).dist) {
                insertIdx = i;
                break;
            }
        }
        if (insertIdx == -1) {
            pairs.add(newPair);
        } else {
            pairs.add(insertIdx, newPair);
        }
    }

    record Vec3D(long x, long y, long z) {}

    record Pairing(Vec3D p1, Vec3D p2, double dist) {}
}

