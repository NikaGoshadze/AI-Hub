import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class WordCount {
    public static void main(String[] args) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        String line = reader.readLine();
        int count = 0;
        if (line != null && !line.isEmpty()) {
            count = line.trim().isEmpty() ? 0 : line.trim().split("\\s+").length;
        }
        System.out.println(count);
    }
}
