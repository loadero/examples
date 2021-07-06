import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.loadero.Loadero;
import com.loadero.model.Group;
import com.loadero.model.GroupParams;
import com.loadero.model.Participant;
import com.loadero.model.ParticipantParams;
import com.loadero.model.Test;
import com.loadero.model.TestParams;
import com.loadero.types.Browser;
import models.GroupConfig;
import models.ParticipantConfig;
import models.TestConfig;
import org.junit.jupiter.api.Assertions;

import java.io.IOException;
import java.time.Duration;
import java.time.LocalTime;

public class TestMain {
  private final String testConfigJsonPath = "src/main/resources/test.json";
  private final String groupConfigJsonPath = "src/main/resources/group.json";
  private final String participantConfigPath = "src/main/resources/participant.json";
  private final Gson gson = new GsonBuilder().create();
  private final String token = System.getenv("LOADERO_API_TOKEN");
  private final int projectId = Integer.parseInt(System.getenv("LOADERO_PROJECT_ID"));
  
  @org.junit.jupiter.api.Test
  public void createTest() throws IOException {
    Loadero.init(token, projectId); // Initializing Loadero's instance
  
    String testConfigJson = FileUtils.readFile(testConfigJsonPath);
    TestConfig testConfig = gson.fromJson(testConfigJson, TestConfig.class);
    Duration startInterval = Duration.ofSeconds(LocalTime.parse(testConfig.getStartInterval()).getSecond());
    Duration participantTimeout = Duration.ofSeconds(LocalTime.parse(testConfig.getParticipantTimeout()).getSecond());
    TestParams testParams = TestParams.builder()
            .withName(testConfig.getTitle())
            .withMode(testConfig.getTestMode())
            .withIncrementStrategy(testConfig.getIncrementStrategy())
            .withScript(testConfig.getScriptPath())
            .withStartInterval(startInterval)
            .withParticipantTimeout(participantTimeout)
            .build();
    Test test = Test.create(testParams);
    Assertions.assertEquals(testConfig.getTestMode(), test.getMode());
    Assertions.assertEquals(testConfig.getTitle(), test.getName());
    Assertions.assertEquals(testConfig.getIncrementStrategy(), test.getIncrementStrategy());
    
    String groupConfigJson = FileUtils.readFile(groupConfigJsonPath);
    GroupConfig groupConfig = gson.fromJson(groupConfigJson, GroupConfig.class);
    GroupParams groupParams = GroupParams.builder()
            .withTestId(test.getId())
            .withName(groupConfig.getTitle())
            .withCount(groupConfig.getCount())
            .build();
    Group group = Group.create(groupParams);
    Assertions.assertEquals(groupConfig.getTitle(), group.getName());
    Assertions.assertEquals(groupConfig.getCount(), group.getCount());
    
    String participantConfigJson = FileUtils.readFile(participantConfigPath);
    ParticipantConfig participantConfig = gson.fromJson(participantConfigJson, ParticipantConfig.class);
    ParticipantParams participantParams = ParticipantParams.builder()
            .withTestId(test.getId())
            .withGroupId(group.getId())
            .withName(participantConfig.getTitle())
            .withComputeUnit(participantConfig.getComputeUnit())
            .withNetwork(participantConfig.getNetwork())
            .withLocation(participantConfig.getLocation())
            .withBrowser(new Browser(participantConfig.getBrowser()))
            .withMediaType(participantConfig.getMediaType())
            .withCount(participantConfig.getCount())
            .build();
    Participant participant = Participant.create(participantParams);
    Assertions.assertEquals(participantConfig.getTitle(), participant.getName());
    Assertions.assertEquals(participantConfig.getCount(), participant.getCount());
    Assertions.assertEquals(participantConfig.getComputeUnit(), participant.getComputeUnit());
  }
}
