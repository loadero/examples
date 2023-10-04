client => {
    // Example of locating elements using CSS selectors
    client
        // Navigate to website google.com
        .url('https://www.google.com')
        // Wait up to 10 seconds until 'body' element is visible)
        .waitForElementVisible('body', 10 * 1000)
        // Type "QA Processes" in the search bar
        .setValue('input[type=text]', 'QA Processes')
         // Trigger search by sending "Enter" key event in the search bar
        .setValue('input[type=text]', client.Keys.ENTER);
}
