// Original article <url>

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
