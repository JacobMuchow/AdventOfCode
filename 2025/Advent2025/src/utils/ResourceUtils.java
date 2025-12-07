package utils;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class ResourceUtils {
    /**
     * Helper to read resource file as one string. Hard crash if it fails.
     */
    public static String readString(String path) {
        try {
            return Files.readString(Path.of(path));
        } catch (IOException e) {
            throw new Error(String.format("Error reading file: %s\n", e.getMessage()));
        }
    }

    /**
     * Helper to read resource file as list of lines. Hard crash if it fails.
     */
    public static List<String> readLines(String path) {
        try {
            return Files.readAllLines(Path.of(path));
        } catch (IOException e) {
            throw new Error(String.format("Error reading file: %s\n", e.getMessage()));
        }
    }

    public static char[][] readCharGrid(String path) {
        try {
            var lines = Files.readAllLines(Path.of(path));
            return lines.stream()
                    .map(String::toCharArray)
                    .toArray(char[][]::new);
        } catch (IOException e) {
            throw new Error(String.format("Error reading file: %s\n", e.getMessage()));
        }
    }
}
