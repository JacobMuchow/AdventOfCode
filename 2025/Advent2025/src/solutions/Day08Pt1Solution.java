package solutions;

import utils.ResourceUtils;
import utils.Runnable;

import java.lang.reflect.Parameter;
import java.sql.Array;
import java.util.*;

public class Day08Pt1Solution implements Runnable {
    @Override
    public void run() {
        final var lines = ResourceUtils.readLines("resources/day08/input.txt");
        final var pairAmount = 1000;

        final List<Vec3D> points = this.parsePoints(lines);

        final List<Pairing> nearestPairs = this.findNearestPairs(points, pairAmount);

        // This will contains a map from "circuit IDs" to list of points in the circuit.
        //Initially, each point ("junction box") is its own individual circuit.
        final Map<String, List<Vec3D>> circuits = new HashMap<>(points.size());
        // We will also have a mapping from point -> Circuit ID for reverse lookup.
        final Map<String, String> circuitLookup = new HashMap<>(points.size());

        for (var point : points) {
            final var circuitID = this.vecHash(point);
            circuits.put(circuitID, new ArrayList<>(List.of(point)));
            circuitLookup.put(circuitID, circuitID);
        }

        // Now, for each pair we need to merge circuits.
        for (var pair : nearestPairs) {
            final var p1 = pair.p1;
            final var p2 = pair.p2;

            final var circuitId1 = circuitLookup.get(this.vecHash(p1));
            final var circuitId2 = circuitLookup.get(this.vecHash(p2));

            if (circuitId1.equals(circuitId2)) continue;

            var c1 = circuits.get(circuitId1);
            var c2 = circuits.get(circuitId2);
            c1.addAll(c2);
            circuits.remove(circuitId2);

            for (var point : c2) {
                circuitLookup.put(this.vecHash(point), circuitId1);
            }
        }

        System.out.printf("Total circuits: %d\n", circuits.size());

        final var sorted = new ArrayList<>(circuits.values());
        sorted.sort(Comparator.comparingInt((List<?> l) -> l.size()).reversed());

        final var product = sorted.get(0).size() * sorted.get(1).size() * sorted.get(2).size();
        System.out.printf("Product: %d\n", product);
    }

    private List<Pairing> findNearestPairs(List<Vec3D> points, int limit) {
        final List<Pairing> nearestPairs = new ArrayList<>(limit);

        for (int i = 0; i < points.size()-1; i++) {
            final var p1 = points.get(i);
            for (int j = i+1; j < points.size(); j++) {
                var p2 = points.get(j);
                var dist = Math.sqrt(Math.powExact((p2.x-p1.x), 2) + Math.powExact((p2.y-p1.y), 2) + Math.powExact((p2.z-p1.z), 2));

                if (nearestPairs.size() < limit) {
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

        return nearestPairs;
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

    private List<Vec3D> parsePoints(List<String> lines) {
        final List<Vec3D> points = new ArrayList<>(lines.size());
        for (var line : lines) {
            final var tokens = line.split(",");
            points.add(new Vec3D(
                    Long.parseLong(tokens[0]),
                    Long.parseLong(tokens[1]),
                    Long.parseLong(tokens[2])
            ));
        }
        return points;
    }

    private String vecHash(Vec3D point) {
        return String.format("%d,%d,%d", point.x, point.y, point.z);
    }

    record Vec3D(long x, long y, long z) {}

    record Pairing(Vec3D p1, Vec3D p2, double dist) {}
}

