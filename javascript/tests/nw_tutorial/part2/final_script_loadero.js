// Original article https://blog.loadero.com/2021/03/19/a-beginners-guide-to-test-automation-with-javascriptnightwatch-js-part-2/

client => {
    client
        .url('https://loadero.com/home')
        .waitForElementVisible('.home', 10 * 1000)
        .waitForElementVisible('.accept', 10 * 1000)
        .click('.accept')
        .setValue('.trial input', 'john.doe@example.com')
        .setValue('.trial input', client.Keys.ENTER)
        .pause(10 * 1000)
        .takeScreenshot('screenshot.png')
        .perform(done => {
            console.log('The script has finished its execution');

            done();
        });
}
