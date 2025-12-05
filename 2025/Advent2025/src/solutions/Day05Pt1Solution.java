package solutions;

import utils.ResourceUtils;
import utils.Runnable;

import java.util.ArrayList;
import java.util.List;

public class Day05Pt1Solution implements Runnable {
    @Override
    public void run() {
        var lines = ResourceUtils.readLines("resources/day05/input.txt");
        // Parse input into list of ranges and IDs.
        var ranges = new ArrayList<Range>();
        var ids = new ArrayList<Long>();
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
        i += 1;
        for (; i < lines.size(); i++) {
            ids.add(Long.parseLong(lines.get(i)));
        }

        // Check how many ranges are fresh
        var totalFresh = 0;
        for (var id : ids) {
            if (isFresh(id, ranges)) {
                totalFresh++;
            }
        }

        System.out.printf("Total fresh: %d\n", totalFresh);
    }

    record Range(Long start, Long end) {};

    private boolean isFresh(Long id, List<Range> ranges) {
        for (var range : ranges) {
            if (id < range.start) return false;
            if (id <= range.end) return true;
        }
        return false;
    }
}
