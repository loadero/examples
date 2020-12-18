# JavaScript examples

Here you can find various Loadero JavaScript test script examples.

Scripts are saved under `tests` directory where they are divided based on the
script theme, for example, if you need examples for scripts from Nightwatch
tutorial blog series, check `nw_tutorial` directory.

## Setup

### Prerequisites

- Text editor of your choice (in Loadero we prefer
  [Visual Studio Code](https://code.visualstudio.com/)).
- [Node.js](https://nodejs.org/) (the latest version is preferable, in this
  example `v14.15.0` will be used).
- [Google Chrome](https://www.google.com/chrome/) and
  [Firefox](https://www.mozilla.org/en-US/firefox/new/) browsers.

### Installation

Download NPM dependencies with the following command

```bash
npm install
```

## Test execution

To run all tests inside `tests` directory, enter

```bash
npm test
```

To run a specfic tests, enter

```bash
npm test -- -t PATH_TO_FILE
```

If you want to run your tests in a different browser (default is Google Chrome),
then specify environment with the following command:

```bash
npm test -- -e ENVIRONMENT
```
