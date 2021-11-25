// Original article https://blog.loadero.com/2021/11/23/a-beginners-guide-to-test-automation-with-javascriptnightwatch-js-part-4/

module.exports = {
    test: client => {
        // GitHub's URL
        const url = 'https://github.com/';

        // Default timeout for `.waitForElementVisible()`
        const timeout = 10 * 1000;

        // Element selectors object
        const selectors = {
            prepare: {
                container: '.application-main',
                signInButton: '[href="/login"]'
            },
            signIn: {
                container: '#login',
                loginInput: '#login_field',
                passwordInput: '#password',
                signInButton: '.js-sign-in-button'
            }
        };

        // Account credentials
        const credentials = {
            email: 'test@example.com',
            password: 'password123'
        };

        // Utility functions
        const waitAndClick = (selector, waitTime = timeout) => {
            client.waitForElementVisible(selector, waitTime).click(selector);
        };

        const waitAndSetValue = (selector, value, waitTime = timeout) => {
            client.waitForElementVisible(selector, waitTime).setValue(selector, value);
        };

        // Main functions
        const prepare = () => {
            const { prepare } = selectors;

            client.url(url).waitForElementVisible(prepare.container, timeout);

            waitAndClick(prepare.signInButton);
        };

        const login = () => {
            const { signIn } = selectors;

            client.waitForElementVisible(signIn.container, timeout);

            waitAndSetValue(signIn.loginInput, credentials.email);
            waitAndSetValue(signIn.passwordInput, credentials.password);

            waitAndClick(signIn.signInButton);
        };

        // Main flow
        prepare();
        login();
    }
};
