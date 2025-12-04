import solutions.Solution;
import solutions.SolutionRunner;

public class Main {
    public static void main(String[] args) {
        var start = System.currentTimeMillis();

        SolutionRunner.run(Solution.Day03Pt2);

        var timeTaken = System.currentTimeMillis() - start;
        System.out.printf("Time taken: %dms\n", timeTaken);
    }
}