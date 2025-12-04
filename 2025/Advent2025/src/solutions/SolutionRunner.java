package solutions;

import utils.Runnable;

import java.util.Map;

public class SolutionRunner {
    private static final Map<Solution, Runnable> solutionMap = Map.ofEntries(
        Map.entry(Solution.Day01Pt1, new Day01Pt1Solution()),
        Map.entry(Solution.Day01Pt2, new Day01Pt2Solution()),
        Map.entry(Solution.Day02Pt1, new Day02Pt1Solution()),
        Map.entry(Solution.Day02Pt2, new Day02Pt2Solution()),
        Map.entry(Solution.Day03Pt1, new Day03Pt1Solution()),
        Map.entry(Solution.Day03Pt2, new Day03Pt2Solution()),
        Map.entry(Solution.Day04Pt1, new Day04Pt1Solution()),
        Map.entry(Solution.Day04Pt2, new Day04Pt2Solution()),
        Map.entry(Solution.Day05Pt1, new Day05Pt1Solution()),
        Map.entry(Solution.Day05Pt2, new Day05Pt2Solution()),
        Map.entry(Solution.Day06Pt1, new Day06Pt1Solution()),
        Map.entry(Solution.Day06Pt2, new Day06Pt2Solution()),
        Map.entry(Solution.Day07Pt1, new Day07Pt1Solution()),
        Map.entry(Solution.Day07Pt2, new Day07Pt2Solution()),
        Map.entry(Solution.Day08Pt1, new Day08Pt1Solution()),
        Map.entry(Solution.Day08Pt2, new Day08Pt2Solution()),
        Map.entry(Solution.Day09Pt1, new Day09Pt1Solution()),
        Map.entry(Solution.Day09Pt2, new Day09Pt2Solution()),
        Map.entry(Solution.Day10Pt1, new Day10Pt1Solution()),
        Map.entry(Solution.Day10Pt2, new Day10Pt2Solution()),
        Map.entry(Solution.Day11Pt1, new Day11Pt1Solution()),
        Map.entry(Solution.Day11Pt2, new Day11Pt2Solution()),
        Map.entry(Solution.Day12Pt1, new Day12Pt1Solution()),
        Map.entry(Solution.Day12Pt2, new Day12Pt2Solution())
    );

    public static void run(Solution solution) {
        var runnable = solutionMap.get(solution);
        if (runnable == null) {
            throw new UnsupportedOperationException(String.format("solutions.Solution %s not yet implemented", solution.name()));
        }
        runnable.run();
    }
}
