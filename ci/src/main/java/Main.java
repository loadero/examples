import com.loadero.Loadero;
import com.loadero.model.Test;
import com.loadero.model.TestRun;
import com.loadero.types.RunStatus;
import java.io.IOException;
import java.time.Duration;

public class Main {
    private static final String TOKEN = System.getenv("ACCESS_TOKEN");
    private static final int PROJECT_ID = Integer.parseInt(System.getenv("PROJECT_ID"));
    private static final int TEST_ID = Integer.parseInt(System.getenv("TEST_ID"));

    public static void main(String[] args) {
        Loadero.init(TOKEN, PROJECT_ID);

        TestRun run;
        try {
            run = Test.launch(TEST_ID);
        } catch (IOException e) {
            throw new RuntimeException("could not launch the test", e);
        }

        try {
            TestRun.poll(TEST_ID, run.getId(), Duration.ofMinutes(1));
        } catch (IOException e) {
            throw new RuntimeException("could not poll test run", e);
        }

        try {
            run = TestRun.read(TEST_ID, run.getId());
        } catch (IOException e) {
            throw new RuntimeException("could not read test run", e);
        }

        if (run.getStatus() != RunStatus.DONE || run.getSuccessRate() != 1) {
            System.out.println("Test failed");
            System.exit(1);
        }

        System.out.println("Test passed");
        System.exit(0);
    }
}
