// Original article https://blog.loadero.com/

module.exports = {
    test: function test(client) {
        client
            .url('https://github.com/')
            .waitForElementVisible('body', 10 * 1000)
            .setValue('.header-search-input', ['Nightwatch', client.Keys.ENTER])
            .pause(5 * 1000)
            .assert.containsText('.repo-list li:nth-of-type(1) div.f4 a', 'nightwatchjs')
            .click('.repo-list li:nth-of-type(1) div.f4 a')
            .waitForElementVisible('.application-main', 10 * 1000)
            .saveScreenshot('nightwathcRepo.png');
    }
};
