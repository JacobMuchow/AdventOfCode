package solutions;

import utils.ResourceUtils;
import utils.Runnable;

public class Day01Pt1Solution implements Runnable {
    @Override
    public void run() {
        var content = ResourceUtils.readLines("resources/day01/test.txt");

        System.out.println("File content:");
        for (var line : content) {
            System.out.println(line);
        }
    }
}
