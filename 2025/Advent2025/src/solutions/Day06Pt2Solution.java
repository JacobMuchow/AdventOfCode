package solutions;

import utils.ResourceUtils;
import utils.Runnable;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Day06Pt2Solution implements Runnable {
    @Override
    public void run() {
        var lines = ResourceUtils.readLines("resources/day06/input.txt");
        var operandLines = lines.subList(0, lines.size()-1);
        var operators = lines.getLast().split("\\s+");
        makeEndsFlush(operandLines);

        var operandGroups = parseOperandGroups(operandLines);

        // Compute a total for each function group and add to grand total.
        long grandTotal = 0L;
        for (var i = 0; i < operators.length; i++) {
            final var operator = operators[i];
            final var operands = operandGroups.get(i);

            long total = operator.equals("+") ? 0 : 1;
            for (var operand : operands) {
                if (operator.equals("+")) {
                    total += operand;
                } else {
                    total *= operand;
                }
            }
            grandTotal += total;
        }

        System.out.printf("Grand total: %d\n", grandTotal);
    }

    private void makeEndsFlush(List<String> operandLines) {
        // Add in trailing white-space at the end so all lines have the same length.
        // This is necessary for our algorithm below to pick up all operands.
        var maxLen = operandLines.stream().mapToInt(String::length).max().orElse(0);
        for (var i = 0; i < operandLines.size(); i++) {
            var line = operandLines.get(i);
            if (line.length() != maxLen) {
                var sb = new StringBuilder(maxLen);
                sb.append(line);
                sb.repeat(' ', maxLen - line.length());
                operandLines.set(i, sb.toString());
            }
        }
    }

    private List<List<Long>> parseOperandGroups(List<String> operandLines) {
        // Parse "groups" of operands by iterating a cursor and parsing individual characters from lines
        // then combining them. When the column is empty, save the current group and start a new one.
        var i = 0;
        List<List<Long>> operandGroups = new ArrayList<>();
        List<Long> operandGroup = new ArrayList<>();
        while (i < operandLines.getFirst().length()) {
            if (isEmptyCol(i, operandLines)) {
                if (!operandGroup.isEmpty()) {
                    operandGroups.add(operandGroup);
                    operandGroup = new ArrayList<>();
                }
            } else {
                StringBuilder sb = new StringBuilder(operandLines.size());
                for (String operandLine : operandLines) {
                    var char_ = operandLine.charAt(i);
                    if (char_ != ' ') {
                        sb.append(char_);
                    }
                }
                operandGroup.add(Long.parseLong(sb.toString()));
            }

            i += 1;
        }

        if (!operandGroup.isEmpty()) {
            operandGroups.add(operandGroup);
        }

        return operandGroups;
    }

    private boolean isEmptyCol(int idx, List<String> rows) {
        for (var row : rows) {
            if (row.charAt(idx) != ' ') {
                return false;
            }
        }
        return true;
    }
}

