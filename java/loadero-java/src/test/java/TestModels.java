import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.loadero.types.BrowserLatest;
import com.loadero.types.Location;
import com.loadero.types.Network;
import com.loadero.types.TestMode;
import models.GroupConfig;
import models.ParticipantConfig;
import models.TestConfig;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class TestModels {
  private final Gson gson = new GsonBuilder().create();
  private final String testConfigJsonPath = "src/main/resources/test.json";
  private final String groupConfigJsonPath = "src/main/resources/group.json";
  private final String participantConfigPath = "src/main/resources/participant.json";
  
  @Test
  public void serializeTestConfig() {
    String testConfigJson = FileUtils.readFile(testConfigJsonPath);
    Assertions.assertNotNull(testConfigJson);
    Assertions.assertFalse(testConfigJson.isEmpty());
    
    TestConfig testConfig = gson.fromJson(testConfigJson, TestConfig.class);
    Assertions.assertNotNull(testConfig);
    Assertions.assertEquals(TestMode.LOAD, testConfig.getTestMode());
  }
  
  @Test
  public void serializeGroupConfig() {
    String groupConfigJson = FileUtils.readFile(groupConfigJsonPath);
    Assertions.assertNotNull(groupConfigJson);
    Assertions.assertFalse(groupConfigJson.isEmpty());
  
    GroupConfig groupConfig = gson.fromJson(groupConfigJson, GroupConfig.class);
    Assertions.assertNotNull(groupConfig);
    Assertions.assertEquals(2, groupConfig.getCount());
  }
  
  @Test
  public void serializeParticipantConfig() {
    String participantConfigJson = FileUtils.readFile(participantConfigPath);
    Assertions.assertNotNull(participantConfigJson);
    Assertions.assertFalse(participantConfigJson.isEmpty());
  
    ParticipantConfig participantConfig = gson.fromJson(participantConfigJson, ParticipantConfig.class);
    Assertions.assertNotNull(participantConfig);
    Assertions.assertEquals(Network.CONNECTION_3G, participantConfig.getNetwork());
    Assertions.assertEquals(BrowserLatest.CHROME_LATEST, participantConfig.getBrowser());
    Assertions.assertEquals(Location.OREGON, participantConfig.getLocation());
  }
}
