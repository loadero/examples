// Original article https://blog.loadero.com/2021/11/23/a-beginners-guide-to-test-automation-with-javascriptnightwatch-js-part-4/

module.exports = {
    test: client => {
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

        // Utility functions
        const waitAndClick = (selector, waitTime = 10 * 1000) => {
            client.waitForElementVisible(selector, waitTime).click(selector);
        };

        const waitAndSetValue = (selector, value, waitTime = 10 * 1000) => {
            client.waitForElementVisible(selector, waitTime).setValue(selector, value);
        };

        // Main functions
        const prepare = () => {
            const { prepare } = selectors;

            client.url('https://github.com/').waitForElementVisible(prepare.container, 10 * 1000);

            waitAndClick(prepare.signInButton);
        };

        const login = () => {
            const { signIn } = selectors;

            client.waitForElementVisible(signIn.container, 10 * 1000);

            waitAndSetValue(signIn.loginInput, 'test@example.com');
            waitAndSetValue(signIn.passwordInput, 'password123');

            waitAndClick(signIn.signInButton);
        };

        // Main flow
        prepare();
        login();
    }
};
