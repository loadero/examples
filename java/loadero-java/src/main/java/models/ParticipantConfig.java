package models;

import com.google.gson.annotations.SerializedName;
import com.loadero.types.BrowserLatest;
import com.loadero.types.ComputeUnit;
import com.loadero.types.Location;
import com.loadero.types.MediaType;
import com.loadero.types.Network;

public final class ParticipantConfig {
  private String title;
  private int count;
  @SerializedName("compute_unit")
  private ComputeUnit computeUnit;
  private BrowserLatest browser;
  private Location location;
  private Network network;
  @SerializedName("media_type")
  private MediaType mediaType;

  public ParticipantConfig(
      String title,
      int count,
      ComputeUnit computeUnit,
      BrowserLatest browser,
      Location location,
      Network network,
      MediaType mediaType) {
    this.title = title;
    this.count = count;
    this.computeUnit = computeUnit;
    this.browser = browser;
    this.location = location;
    this.network = network;
    this.mediaType = mediaType;
  }

  public String getTitle() {
    return title;
  }

  public void setTitle(String title) {
    this.title = title;
  }

  public int getCount() {
    return count;
  }

  public void setCount(int count) {
    this.count = count;
  }

  public ComputeUnit getComputeUnit() {
    return computeUnit;
  }

  public void setComputeUnit(ComputeUnit computeUnit) {
    this.computeUnit = computeUnit;
  }

  public BrowserLatest getBrowser() {
    return browser;
  }

  public void setBrowser(BrowserLatest browser) {
    this.browser = browser;
  }

  public Location getLocation() {
    return location;
  }

  public void setLocation(Location location) {
    this.location = location;
  }

  public Network getNetwork() {
    return network;
  }

  public void setNetwork(Network network) {
    this.network = network;
  }

  public MediaType getMediaType() {
    return mediaType;
  }

  public void setMediaType(MediaType mediaType) {
    this.mediaType = mediaType;
  }

  @Override
  public String toString() {
    return "ParticipantConfig{"
        + "title='"
        + title
        + '\''
        + ", count="
        + count
        + ", computeUnit="
        + computeUnit
        + ", browser="
        + browser
        + ", location="
        + location
        + ", network="
        + network
        + ", mediaType="
        + mediaType
        + '}';
  }
}
