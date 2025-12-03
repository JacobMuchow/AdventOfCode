package solutions;

import utils.Runnable;

import java.util.Map;

public class SolutionRunner {
    private static final Map<Solution, Runnable> solutionMap = Map.of(
        Solution.Day01Pt1, new Day01Pt1Solution()
    );

    public static void run(Solution solution) {
        var runnable = solutionMap.get(solution);
        if (runnable == null) {
            throw new UnsupportedOperationException(String.format("solutions.Solution %s not yet implemented", solution.name()));
        }
        runnable.run();
    }
}
