// Original article https://blog.loadero.com/

module.exports = {
    test: client => {
        client
            .url('https://github.com/')
            // .waitForElementVisible('body', 10 * 1000)
            .setValue('.header-search-input', ['Nightwatch', client.Keys.ENTER])
            .waitForElementVisible('.repo-list', 10 * 1000)
            .assert.containsText('.repo-list li:nth-of-type(1) div.f4 a', 'nightwatchjs')
            .saveScreenshot('repoList.png')
            .pause(5 * 1000);
    }
};
