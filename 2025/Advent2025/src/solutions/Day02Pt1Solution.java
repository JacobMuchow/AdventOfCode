package solutions;

import utils.ResourceUtils;
import utils.Runnable;

import java.util.ArrayList;

public class Day02Pt1Solution implements Runnable {
    @Override
    public void run() {
        var input = ResourceUtils.readString("resources/day02/input.txt");

        var pidRanges = input.split(",");
        var total = 0L;
        for (var pidRange : pidRanges) {
            var parts = pidRange.split("-");
            var firstPid = Long.parseLong(parts[0]);
            var lastPid = Long.parseLong(parts[1]);

            if (lastPid < firstPid) {
                var swap = firstPid;
                firstPid = lastPid;
                lastPid = swap;
            }

            for (var pid = firstPid; pid <= lastPid; pid++) {
                if (!isValid(String.valueOf(pid))) {
                    total += pid;
                }
            }
        }

        System.out.printf("Total: %d\n", total);
    }

    private boolean isValid(String pid) {
        // PIDs cannot start with 0
        if (pid.startsWith("0")) {
            return false;
        }
        // Odd length IDs are all OK.
        if (pid.length() % 2 != 0) {
            return true;
        }
        // Check for repeating sequence, if not repeating then it's valid.
        var half = pid.length() / 2;
        for (var i = 0; i < half; i++) {
            if (pid.charAt(i) != pid.charAt(i+half)) {
                return true;
            }
        }
        return false;
    }
}
