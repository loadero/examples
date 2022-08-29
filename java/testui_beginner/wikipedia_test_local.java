import static testUI.UIOpen.open;
import static testUI.Utils.By.byCssSelector;
import static testUI.Utils.By.byId;
import static testUI.elements.TestUI.E;
import static testUI.collections.TestUI.EE;

import testUI.collections.UICollection;
import testUI.elements.UIElement;
import org.junit.Test;

public class Wikipedia {
    @Test
    public void test() {

        //HTML elements that will be used
        UIElement searchInput = E(byCssSelector("input#searchInput"));
        UIElement searchButton = E(byId("searchButton"));
        UIElement todaysArticle = E(byCssSelector("#mp-tfa p"));
        UIElement pageContainer = E(byId("content"));

        //open url and wait until page container is visible
        open("https://en.wikipedia.org/wiki/Main_Page");
        pageContainer.waitFor(10).untilIsVisible();

        //get text of today's article
        String text = todaysArticle.getText();
        System.out.printf("Todays featured article is:\n %s\n", text);

        // input text in search input field
        searchInput.waitFor(10).untilIsVisible().sendKeys("Selenium Webdriver");
        searchButton.click();
        // alternative: searchInput.sendKeys(Keys.ENTER);

        //take a screenshot
        pageContainer.waitFor(10).untilIsVisible().saveScreenshot("screenshot.png");

        //save all search results titles in a `collection`
        UICollection collection = EE(byCssSelector(".mw-search-result-heading"));
        String firstResult = collection.first().getText();
        System.out.printf("First result is:\n%s\n", firstResult);

        String anotherResult = collection.findByText("IT").getText();
        System.out.printf("Result containing 'IT' is:\n%s\n", anotherResult);
    }
}
