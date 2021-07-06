import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class FileUtils {
  public static String readFile(String path) {
    String result = "";

    try {
      Path filePath = Path.of(path);
      result = Files.readString(filePath);
    } catch (IOException ex) {
      ex.printStackTrace();
    }

    return result;
  }
}
