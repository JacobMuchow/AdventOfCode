package solutions;

import utils.ResourceUtils;
import utils.Runnable;

public class Day02Pt2Solution implements Runnable {
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
        // We need to check for any length repeating sequence, repeating 2+ times.
        // To optimize slightly (?), we start with largest possible sequence (2x), then work down to sequence length of 1.
        var largestSeq = pid.length() / 2;
        for (var seqLen = largestSeq; seqLen >= 1; seqLen -= 1) {
            // We only need to test if this length of the ID is divisible by the sequence length we want to test.
            // ex) no point in testing sequence length of 4 in a 9 digit ID.
            if (pid.length() % seqLen == 0) {
                // If there is a repeating sequence found, then return "false" - the ID is invalid.
                if (testForRepeatingSequence(pid, seqLen)) {
                    return false;
                }
            }
        }
        // Once all sequence lengths were tested, if we didn't return false, then the ID is valid.
        return true;
    }

    // This is a modified version of our original test that things about the check as "cursors"
    // Given a sequence length, and PID length, we know how many other spots/"cursors" we need to check
    // per each index of the sequence. If any given comparison doesn't match, then we return "false" not repeating.
    // @returns true if there is a repeating sequence of the given length. False if not.
    private boolean testForRepeatingSequence(String pid, Integer seqLength) {
        var numCursors = pid.length() / seqLength;
        for (var i = 0; i < seqLength; i++) {
            var match = pid.charAt(i);

            for (var j = 1; j < numCursors; j++) {
                if (pid.charAt(j * seqLength + i) != match) {
                    return false;
                }
            }
        }

        return true;
    }
}
