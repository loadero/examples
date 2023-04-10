# Loadero
Python generator, manager and runner for automated Loadero tests

## Prerequisites

- Install Python 3 (Python version should be >= v.3.10)

  ```bash
  brew install python@3.10
  ```

- Create virtual environment

  ```bash
  python -m venv venv
  ```

- Activate virtual enviornment
  ```
  source venv/bin/activate
  ```

- Install depenendencies
  ```bash
  pip install -r requirements.txt
  ```

- When done modifying virtual environment, leave it

  ```bash
  deactivate
  ```

- Or use the shellscript to setup and run the tests. Example:

  ```bash
  ./script.sh <auth_token> <project_id> <test_ids> <timeout>
  ```

## Generate Loadero tests

- Generate Loadero test

  ```
  python test_generator.py \
  --access_token {ACCESS_TOKEN} \
  --project_id {PROJECT_ID}
  ```

| CLI argument | Mandatory | Description |
| --- | --- | --- |
| access_token| Yes | Project access token where tests will be run |
| project_id | Yes | Project ID where tests will be run  |

## Run Loadero tests

- Run Loadero tests by passing test ids list

  ```
  python test_runner.py \
  --access_token {ACCESS_TOKEN} \
  --project_id {PROJECT_ID} \
  --test_ids {TEST_ID1} {TEST_ID2} {TEST_IDN}} \
  --timeout {TIMEOUT}
  ```

- Run Loadero tests by passing suite

  ```
  python test_runner.py \
  --access_token {ACCESS_TOKEN} \
  --project_id {PROJECT_ID} \
  --suite {SUITE_NAME} \
  --timeout {TIMEOUT}
  ```

- Run Loadero tests by passing test ids list and suite (It there are duplicated test ids, the test with that particular id will be runned once.)

  ```
  python test_runner.py \
  --access_token {ACCESS_TOKEN} \
  --project_id {PROJECT_ID} \
  --test_ids {TEST_ID1} {TEST_ID2} {TEST_IDN} \
  --suite {SUITE_NAME} \
  --timeout {TIMEOUT}
  ```

| CLI argument | Mandatory | Description |
| --- | --- | --- |
| access_token| Yes | Project access token where tests will be run |
| project_id | Yes | Project ID where tests will be run  |
| test_ids | No | Tests identifier listing |
| suite | No | Name of the suite in project configuration that groups the tests |
| timeout | No | Timeout for test execution (defaults to 3600s) |

 ## Manage Loadero tests

- Initialize local Loadero project

  ```
  python test_manager.py \
  --access_token_from {ACCESS_TOKEN} \
  --project_id_from {PROJECT_ID} \
  --action init
  ```

!!! Note: The init action must be done before the first backup!

- Back up all Loadero test(s) from source Loadero project

  ```
  python test_manager.py \
  --access_token_from {ACCESS_TOKEN} \
  --project_id_from {PROJECT_ID} \
  --action backup
  ```

- Back up certain Loadero test(s) from source Loadero project by passing test ids

  ```
  python test_manager.py \
  --access_token_from {ACCESS_TOKEN} \
  --project_id_from {PROJECT_ID} \
  --test_ids {TEST_ID1} {TEST_ID2} {TEST_IDN} \
  --action backup
  ```

- Back up certain Loadero test(s) from source Loadero project by passing suite

  ```
  python test_manager.py \
  --access_token_from {ACCESS_TOKEN} \
  --project_id_from {PROJECT_ID} \
  --suite {SUITE_NAME} \
  --action backup
  ```

- Back up certain Loadero test(s) from source Loadero project by passing test ids and suite (It there are duplicated test ids, the test with that particular id will be backup once.)

  ```
  python test_manager.py \
  --access_token_from {ACCESS_TOKEN} \
  --project_id_from {PROJECT_ID} \
  --test_ids {TEST_ID1} {TEST_ID2} {TEST_IDN} \
  --suite {SUITE_NAME} \
  --action backup
  ```

- Restore all local test(s) to destination Loadero project

  ```
  python test_manager.py \
  --local_project_id {PROJECT_ID_FOR_LOCAL_FILES} \
  --access_token_to {ACCESS_TOKEN} \
  --project_id_to {PROJECT_ID} \
  --action restore
  ```

- Restore certain local test(s) to destination Loadero project by passing local test ids

  ```
  python test_manager.py \
  --local_project_id {PROJECT_ID_FOR_LOCAL_FILES} \
  --access_token_to {ACCESS_TOKEN} \
  --project_id_to {PROJECT_ID} \
  --test_ids {TEST_ID1} {TEST_ID2} {TEST_IDN} \
  --action restore
  ```

- Restore certain local test(s) to destination Loadero project by passing suite

  ```
  python test_manager.py \
  --local_project_id {PROJECT_ID_FOR_LOCAL_FILES} \
  --access_token_to {ACCESS_TOKEN} \
  --project_id_to {PROJECT_ID} \
  --suite {SUITE_NAME} \
  --action restore
  ```

- Restore certain local test(s) to destination Loadero project by passing test ids and suite (It there are duplicated test ids, the test with that particular id will be restored once.)

  ```
  python test_manager.py \
  --local_project_id {PROJECT_ID_FOR_LOCAL_FILES} \
  --access_token_to {ACCESS_TOKEN} \
  --project_id_to {PROJECT_ID} \
  --test_ids {TEST_ID1} {TEST_ID2} {TEST_IDN} \
  --suite {SUITE_NAME} \
  --action restore
  ```

- Migrate all Loadero test(s)

  ```
  python test_manager.py
  --access_token_from {ACCESS_TOKEN} \
  --project_id_from {PROJECT_ID} \
  --access_token_to {ACCESS_TOKEN} \
  --project_id_to {PROJECT_ID} \
  --action migrate
  ```

- Migrate certain Loadero test(s) by passing Loadero test ids

  ```
  python test_manager.py \
  --access_token_from {ACCESS_TOKEN} \
  --project_id_from {PROJECT_ID} \
  --access_token_to {ACCESS_TOKEN} \
  --project_id_to {PROJECT_ID} \
  --test_ids {TEST_ID1} {TEST_ID2} {TEST_IDN} \
  --action migrate
  ```

- Migrate certain Loadero test(s) by passing local suite

  ```
  python test_manager.py \
  --access_token_from {ACCESS_TOKEN} \
  --project_id_from {PROJECT_ID} \
  --access_token_to {ACCESS_TOKEN} \
  --project_id_to {PROJECT_ID} \
  --suite {SUITE_NAME} \
  --action migrate
  ```

- Clone certain Loadero test(s) by passing Loadero test ids and suite (If there are duplicated test ids, the test with that particular id will be cloned once.)

  ```
  python test_manager.py \
  --access_token_from {ACCESS_TOKEN} \
  --project_id_from {PROJECT_ID} \
  --access_token_to {ACCESS_TOKEN} \
  --project_id_to {PROJECT_ID} \
  --test_ids {TEST_ID1} {TEST_ID2} {TEST_IDN} \
  --suite {SUITE_NAME} \
  --action clone
  ```

- Clone all Loadero test(s)

  ```
  python test_manager.py \
  --access_token_from {ACCESS_TOKEN} \
  --project_id_from {PROJECT_ID} \
  --access_token_to {ACCESS_TOKEN} \
  --project_id_to {PROJECT_ID} \
  --action clone
  ```

- Clone certain Loadero test(s) by passing Loadero test ids

  ```
  python test_manager.py \
  --access_token_from {ACCESS_TOKEN} \
  --project_id_from {PROJECT_ID} \
  --access_token_to {ACCESS_TOKEN} \
  --project_id_to {PROJECT_ID} \
  --test_ids {TEST_ID1} {TEST_ID2} {TEST_IDN} \
  --action clone
  ```

- Clone certain Loadero test(s) by passing local suite

  ```
  python test_manager.py \
  --access_token_from {ACCESS_TOKEN} \
  --project_id_from {PROJECT_ID} \
  --access_token_to {ACCESS_TOKEN} \
  --project_id_to {PROJECT_ID} \
  --suite {SUITE_NAME} \
  --action clone
  ```

- Clone certain Loadero test(s) by passing Loadero test ids and suite (It there are duplicated test ids, the test with that particular id will be cloned once.)

  ```
  python test_manager.py \
  --access_token_from {ACCESS_TOKEN} \
  --project_id_from {PROJECT_ID} \
  --access_token_to {ACCESS_TOKEN} \
  --project_id_to {PROJECT_ID} \
  --test_ids {TEST_ID1} {TEST_ID2} {TEST_IDN} \
  --suite {SUITE_NAME} \
  --action clone
  ```

| CLI argument | Action | Mandatory | Description |
| --- | --- | --- | --- |
| access_token_from | init, backup, clone | Yes | Source project's access token from which the tests will be backed up |
| project_id_from | init, backup, clone | Yes | Source project id from which the tests will be backed up |
| access_token_to| restore, clone  | Yes | Destination project's access token in which the tests will be restored |
| project_id_to | restore, clone | Yes | Destination project id in which the tests will be restored |
| local_project_id | restore | Yes | Local project's ID from which the tests will be restored |
| test_ids | backup, restore, clone | No | Test ids to be backed up and restored (if not specified all test will be covered) |
| suite | backup, restore, clone | No | Suite name (if not specified all test will be covered), read from {PROJECT_ID}_{PROJECT_NAME}.json file |
| action | init, backup, restore, clone | Yes | backup, restore or clone (includes both backup and restore) |
| delete_source_test | backup, clone | No | Deletes the tests with test ids in the cource project (if not specified False) |
| ignore_project_language_check | restore, clone | No | Ignores different project languages (if not specified False) |
| overwrite_suite | backup, clone | No | Overwrites existing suite (if not specified False) |

## Statistics

- Get statistics for particular Loadero test executions

  ```
  python loadero_statistics.py \
  --access_token {ACCESS_TOKEN} \
  --project_id {PROJECT_ID} \
  --test_ids {TEST_ID1 TEST_ID2 TEST_IDN} \
  --n {NUMBER_OF_TEST_RUNS} \
  --offset {OFFSET}
  ```

| CLI argument | Mandatory | Description |
| --- | --- | --- |
| access_token| Yes | Project access token where |
| project_id | Yes | Project ID |
| test_ids | Yes | Tests identifier listing |
| n | No | Number of test runs |
| offset | No | Offset |

## Test case data
- project_id_info.json - Default information about project in json format
- test.json - Default information about test in json format
- script.<.js | .py | .java> - Test script extension depends on the project's programming language
- groups.json - Test's groups in json format
- participants.json - Test's participants in json format
- asserts.json - Test's asserts in json format
- assert_preconditions.json - Assert preconditions for assert with assert_id

## Examples
### Local backup and update on the same project
- Back up the test locally
```
python test_manager.py --access_token_from {PROJECT_A_ACCESS_TOKEN} --project_id_from {PROJECT_A_ID} --test_ids {TEST_IDS_LIST} --action backup
```
- Edit the local backup by changing the test's JSON files
- Restore it to the same project
```
python test_manager.py --access_token_to {PROJECT_A_ACCESS_TOKEN} --project_id_to {PROJECT_A_ID} --test_ids {TEST_IDS_LIST} --action restore --local_project_id {LOCAL_PROJECT_ID}
```
Loadero test on the same project should be updated with the local changes 

### Clone tests to another project
- Clone the test from project A to project B
```
python test_manager.py --access_token_from {PROJECT_A_ACCESS_TOKEN} --access_token_to {PROJECT_B_ACCESS_TOKEN} --project_id_from {PROJECT_A_ID} --project_id_to {PROJECT_B_ID} --test_ids {TEST_IDS_LIST} --action clone
```
!!! Note: If the test is not required in project A and migration is one way use `--delete_source_test True` to delete the test from project A.

!!! Note: If the test can be cloned to project with different script language use `--ignore_project_language_check True`
After the clone, there will be a local copy of the same test that is previously cloned and there will be a new test in project B.

- Update the tests after cloning

```
python test_manager.py --access_token_to {PROJECT_B_ACCESS_TOKEN} --project_id_to {PROJECT_B_ID} --test_ids {TEST_IDS_LIST} --action restore --local_project_id {LOCAL_PROJECT_ID_FOR_PROJECT_B}
```
After restore the test on project B will be updated with local changes.

### Migrate tests to another project
- Migrate the test from project A to project B
```
python test_manager.py --access_token_to {PROJECT_B_ACCESS_TOKEN} --project_id_to {PROJECT_B_ID} --access_token_from {PROJECT_A_ACCESS_TOKEN}  --project_id_from {PROJECT_A_ID} --action migrate --suite {SUITE_NAME_FROM_PROJECT_A} --overwrite_suite True 
```
!!! Note: If the test is not specified in the suite use `--test_ids {TEST_IDS}` to add the test for migration.
!!! Note: If the test is not required in project A and migration is one way use `--delete_source_test True` to delete the test from project A.

!!! Note: If the test can be cloned to project with different script language use `--ignore_project_language_check True`
After the clone, there will be a local copy of the same test that is previously cloned and there will be a new test in project B.

After migration the test from project B will be backed up locally.

## Linter
  ```
  pylint ./*/*.py
  ```

## Debugging

- For debugging purpose there is CLI parameter log_level.

`--log_level` - if not specified info, can be `['info', 'INFO', 'debug', 'DEBUG']`
