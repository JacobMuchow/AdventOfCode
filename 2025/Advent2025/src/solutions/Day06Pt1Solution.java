package solutions;

import utils.ResourceUtils;
import utils.Runnable;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Day06Pt1Solution implements Runnable {
    @Override
    public void run() {
        var lines = ResourceUtils.readLines("resources/day06/input.txt");

        List<long[]> operandRows = new ArrayList<>();
        String[] operators = new String[] {};

        for (var i = 0; i < lines.size(); i++) {
            final var line = lines.get(i).trim();
            final var tokens = line.split("\\s+");

            // All but last row are operands
            if (i < lines.size()-1) {
                long[] operands = Arrays.stream(tokens).mapToLong(Long::parseLong).toArray();
                operandRows.add(operands);
            } else {
                operators = tokens;
            }
        }

        long grandTotal = 0L;
        for (var i = 0; i < operators.length; i++) {
            final String operator = operators[i];

            long total = operator.equals("+") ? 0 : 1;
            for (var j = 0; j < operandRows.size(); j++) {
                if (operator.equals("+")) {
                    total += operandRows.get(j)[i];
                } else {
                    total *= operandRows.get(j)[i];
                }
            }
            grandTotal += total;
        }

        System.out.printf("Grand total: %d\n", grandTotal);
    }
}

