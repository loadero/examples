// Original article https://blog.loadero.com/2021/06/22/a-beginners-guide-to-test-automation-with-javascriptnightwatch-js-part-3

client => {
    let text;

    client
        .url('https://duckduckgo.com/')
        .perform(() => {
            text = 'first'; // assigns 'first' to text
        })
        .setValue('#search_form_input_homepage', text)
        .getValue('#search_form_input_homepage', ({ value }) => console.log(value))
        .clearValue('#search_form_input_homepage') // clears input field
        .perform(() => client.setValue('#search_form_input_homepage', text))
        .getValue('#search_form_input_homepage', ({ value }) => console.log(value));

    console.log('second');
}
