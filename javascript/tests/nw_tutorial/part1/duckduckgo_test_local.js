// Original article https://blog.loadero.com/

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