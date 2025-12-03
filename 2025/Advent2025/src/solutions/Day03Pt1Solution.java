package solutions;

import utils.ResourceUtils;
import utils.Runnable;

public class Day03Pt1Solution implements Runnable {
    @Override
    public void run() {
        var input = ResourceUtils.readString("resources/day03/test.txt");
        System.out.println(input);
    }
}
