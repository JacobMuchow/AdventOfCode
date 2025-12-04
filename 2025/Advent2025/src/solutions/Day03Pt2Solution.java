package solutions;

import utils.ResourceUtils;
import utils.Runnable;

public class Day03Pt2Solution implements Runnable {
    @Override
    public void run() {
        var lines = ResourceUtils.readLines("resources/day03/input.txt");

        long maxJoltage = 0;

        for (var line : lines) {
            maxJoltage += calculateMaxJoltage(line, 12);
        }

        System.out.printf("Max joltage: %d\n", maxJoltage);
    }

    private long calculateMaxJoltage(String bank, int numDigits) {
        int maxVal = -1;
        int maxIdx = -1;

        for (var i = 0; i < bank.length()-(numDigits-1); i++) {
            var joltage = Integer.parseInt(bank.substring(i, i+1));
            if (joltage > maxVal) {
                maxVal = joltage;
                maxIdx = i;
                if (joltage == 9) break;
            }
        }

        if (numDigits > 1) {
            long curValue = (long) maxVal * Math.powExact(10L, numDigits-1);

            var bankPart = bank.substring(maxIdx+1);
            return curValue + calculateMaxJoltage(bankPart, numDigits-1);
        }

        return maxVal;
    }
}
