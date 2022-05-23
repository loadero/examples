import * as core from '@actions/core';
import fetch from 'node-fetch';

// Loadero API base URL
const BASE_URL = 'https://api.loadero.com/v2/projects';
// The ID of the project we are working with
const PROJECT_ID = process.env.PROJECT_ID;
// The ID of the test we want to run
const TEST_ID = process.env.TEST_ID;
// Request options with authorization header
const OPTIONS = {
    headers: {
        Authorization: `LoaderoAuth ${process.env.ACCESS_TOKEN}`
    }
};

const startTest = async () => {
    const url = ` ${BASE_URL}/${PROJECT_ID}/tests/${TEST_ID}/runs/`;
    const response = await fetch(url, { ...OPTIONS, method: 'POST' });

    return response.json();
};

const checkTestStatus = async testID => {
    let timeout;

    core.info('Checking status of test ...');

    try {
        const url = `${BASE_URL}/${PROJECT_ID}/runs/?filter_finished=false`;
        const response = await fetch(url, { ...OPTIONS, method: 'GET' });
        const data = await response.json();
        const runningTest = data.results.find(test => test.id === testID);

        if (!runningTest) {
            core.setFailed('Test failed', data.results.length);

            return;
        }

        if (runningTest.success_rate === 1) {
            core.notice('Test success');

            return;
        }

        timeout = setTimeout(() => checkTestStatus(testID), 5000);
    } catch (error) {
        core.setFailed('Something went wrong');
        clearTimeout(timeout);
    }
};

// Run test
startTest()
    .then(test => {
        checkTestStatus(test.id);
    })
    .catch(error => {
        core.setFailed('Test failed', error);
    });
