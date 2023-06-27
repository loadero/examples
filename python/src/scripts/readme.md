# Download everything script usage

## 1. setup

Prerequisite - working python environmet.

Install requirements

```sh
pip install -r requirements.txt
```

## 2. usage

The script has the following arguments

- `--project_id` ID of the project that the access token is created for
- `--access_token` project access token, contact support to create one
- `--output_dir` where to store output
- `--run_id` ID of run to download
- `--test_id` ID of test to download

When running the script specifying `project_id`, `access_token`, `output_dir` is
required.

Must specify `run_id` or `test_id` or both.
