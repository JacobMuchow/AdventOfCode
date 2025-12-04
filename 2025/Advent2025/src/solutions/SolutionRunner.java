package solutions;

import utils.Runnable;

import java.util.Map;

public class SolutionRunner {
    private static final Map<Solution, Runnable> solutionMap = Map.of(
        Solution.Day01Pt1, new Day01Pt1Solution(),
        Solution.Day01Pt2, new Day01Pt2Solution(),
        Solution.Day02Pt1, new Day02Pt1Solution(),
        Solution.Day02Pt2, new Day02Pt2Solution(),
        Solution.Day03Pt1, new Day03Pt1Solution(),
        Solution.Day03Pt2, new Day03Pt2Solution(),
        Solution.Day04Pt1, new Day04Pt1Solution(),
        Solution.Day04Pt2, new Day04Pt2Solution()
    );

    public static void run(Solution solution) {
        var runnable = solutionMap.get(solution);
        if (runnable == null) {
            throw new UnsupportedOperationException(String.format("solutions.Solution %s not yet implemented", solution.name()));
        }
        runnable.run();
    }
}
