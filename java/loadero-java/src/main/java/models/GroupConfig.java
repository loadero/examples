package models;

public final class GroupConfig {
  private String title;
  private int count;

  public GroupConfig(String title, int count) {
    this.title = title;
    this.count = count;
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

  @Override
  public String toString() {
    return "GroupConfig{" + "title='" + title + '\'' + ", count=" + count + '}';
  }
}
