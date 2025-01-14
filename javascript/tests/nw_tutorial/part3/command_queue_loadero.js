// Original article https://blog.loadero.com/2021/06/22/a-beginners-guide-to-test-automation-with-javascriptnightwatch-js-part-3

client => {
    let text;

    client
        .url('https://duckduckgo.com/')
        .perform(() => {
            text = 'first'; // assigns 'first' to text
        })
        .click('#searchbox_input')
        .setValue('#searchbox_input', text)
        .getValue('#searchbox_input', ({ value }) => console.log(value))
        .clearValue('#searchbox_input') // clears input field
        .perform(() => client.setValue('#searchbox_input', text))
        .getValue('#searchbox_input', ({ value }) => console.log(value));

    console.log('second');
}
