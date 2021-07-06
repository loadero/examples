package models;

import com.google.gson.annotations.SerializedName;
import com.loadero.types.IncrementStrategy;
import com.loadero.types.TestMode;

public final class TestConfig {
  private String title;
  @SerializedName("test_mode")
  private TestMode testMode;
  @SerializedName("increment_strategy")
  private IncrementStrategy incrementStrategy;
  @SerializedName("start_interval")
  private String startInterval;
  @SerializedName("participant_timeout")
  private String participantTimeout;
  @SerializedName("script_path")
  private String scriptPath;

  public TestConfig(
      String title,
      TestMode testMode,
      IncrementStrategy incrementStrategy,
      String startInterval,
      String participantTimeout,
      String scriptPath) {
    this.title = title;
    this.testMode = testMode;
    this.incrementStrategy = incrementStrategy;
    this.startInterval = startInterval;
    this.participantTimeout = participantTimeout;
    this.scriptPath = scriptPath;
  }

  public String getTitle() {
    return title;
  }

  public void setTitle(String title) {
    this.title = title;
  }

  public TestMode getTestMode() {
    return testMode;
  }

  public void setTestMode(TestMode testMode) {
    this.testMode = testMode;
  }

  public IncrementStrategy getIncrementStrategy() {
    return incrementStrategy;
  }

  public void setIncrementStrategy(IncrementStrategy incrementStrategy) {
    this.incrementStrategy = incrementStrategy;
  }

  public String getStartInterval() {
    return startInterval;
  }

  public void setStartInterval(String startInterval) {
    this.startInterval = startInterval;
  }

  public String getParticipantTimeout() {
    return participantTimeout;
  }

  public void setParticipantTimeout(String participantTimeout) {
    this.participantTimeout = participantTimeout;
  }

  public String getScriptPath() {
    return scriptPath;
  }

  public void setScriptPath(String scriptPath) {
    this.scriptPath = scriptPath;
  }

  @Override
  public String toString() {
    return "TestConfig{"
        + "title='"
        + title
        + '\''
        + ", testMode="
        + testMode
        + ", incrementStrategy="
        + incrementStrategy
        + ", startInterval='"
        + startInterval
        + '\''
        + ", participantTimeout='"
        + participantTimeout
        + '\''
        + ", scriptPath='"
        + scriptPath
        + '\''
        + '}';
  }
}
