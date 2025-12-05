package solutions;

import utils.ResourceUtils;
import utils.Runnable;

import java.util.ArrayList;
import java.util.List;

public class Day05Pt2Solution implements Runnable {
    @Override
    public void run() {
        var lines = ResourceUtils.readLines("resources/day05/input.txt");

        // Parse input into an ordered list of ranges (IDs are ignored).
        var ranges = new ArrayList<Range>();
        var i = 0;
        for (; i < lines.size(); i++) {
            var line = lines.get(i);
            if (line.isEmpty()) break;

            var parts = line.split("-");
            var newRange = new Range(Long.parseLong(parts[0]), Long.parseLong(parts[1]));

            // Insert new range in order
            var insertAt = -1;
            for (var j = 0; j < ranges.size(); j++) {
                if (ranges.get(j).start > newRange.start) {
                    insertAt = j;
                    break;
                }
            }
            if (insertAt >= 0) {
                ranges.add(insertAt, newRange);
            } else {
                ranges.add(newRange);
            }
        }

        // Merge overlapping ranges together
        i = 0;
        while (i < ranges.size()-1) {
            var cur = ranges.get(i);
            var next = ranges.get(i+1);

            if (next.start <= cur.end) {
                var merged = new Range(
                    Math.min(cur.start, next.start),
                    Math.max(cur.end, next.end)
                );
                ranges.add(i, merged);
                ranges.remove(i+1);
                ranges.remove(i+1);
            } else {
                i += 1;
            }
        }

        // Sum range total of all ranges
        var rangeTotal = 0L;
        for (var range : ranges) {
            rangeTotal += range.end - range.start + 1;
        }

        System.out.printf("\nTotal possible fresh IDs: %d\n", rangeTotal);
    }

    record Range(Long start, Long end) {};
}
