package solutions;

import utils.ResourceUtils;
import utils.Runnable;

public class Day04Pt1Solution implements Runnable {
    @Override
    public void run() {
        var lines = ResourceUtils.readString("resources/day04/test.txt");

        System.out.println(lines);
    }
}
