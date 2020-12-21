// Original article https://blog.loadero.com/2020/12/18/a-beginners-guide-to-test-automation-with-javascriptnightwatch-js-part-1/

module.exports = {
    test: client => {
        client
            .url('https://duckduckgo.com/')
            .waitForElementVisible('#content_homepage', 10 * 1000)
            .setValue('#search_form_input_homepage', 'Nightwatch.js')
            .setValue('#search_form_input_homepage', client.Keys.ENTER)
            .assert.containsText('#r1-0 .result__title', 'Nightwatch.js')
            .click('#r1-0 .result__title')
            .saveScreenshot('NightwatchJS.png')
            .pause(5 * 1000);
    }
};
