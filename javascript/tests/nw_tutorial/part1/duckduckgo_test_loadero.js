client => {
    // Original article https://blog.loadero.com/2020/12/18/a-beginners-guide-to-test-automation-with-javascriptnightwatch-js-part-1/

    client
        .url('https://duckduckgo.com/')
        .waitForElementVisible('[data-testid=hero]', 10 * 1000)
        .click('#searchbox_input')
        .setValue('#searchbox_input', ['Nightwatch.js', client.Keys.ENTER])
        .waitForElementVisible('#r1-0 p:has(+ a)')
        .assert.containsText('#r1-0 p:has(+ a)', 'Nightwatch.js')
        .click('#r1-0 p:has(+ a)')
        .takeScreenshot('NightwatchJS.png')
        .pause(5 * 1000);
}
