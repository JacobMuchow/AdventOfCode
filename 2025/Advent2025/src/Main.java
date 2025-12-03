import solutions.Solution;
import solutions.SolutionRunner;

void main() {
    var start = System.currentTimeMillis();

    SolutionRunner.run(Solution.Day01Pt1);

    var timeTaken = System.currentTimeMillis() - start;
    System.out.printf("Time taken: %dms\n", timeTaken);
}
