// Original article https://blog.loadero.com/2021/03/19/a-beginners-guide-to-test-automation-with-javascriptnightwatch-js-part-2/

client => {
    client
        .url('https://github.com/')
        .waitForElementVisible('.search-input-container', 10 * 1000)
        .click('.search-input-container')
        .setValue('.FormControl-input', 'Nightwatch')
        .click('.ActionListItem')
        .assert.textContains('a .search-match', 'nightwatch')
        .click('.search-title a')
        .pause(5 * 1000)
        .takeScreenshot('nightwatch.png')
        .perform(done => {
            console.log('The script has finished its execution');

            done();
        });
}
