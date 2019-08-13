# Getting Data from the Learnosity API

## TL;DR: Use our script to get data

You'll need **Python 3.6** to make this work 😇

From this directory:

1.  Install the requirements:

    ```bash
    # Make sure Python 3.6 or higher and the pip package manager
    # are on your path. Then, from this directory:
    pip install -r requirements.txt
    ```

1.  Create a `secrets.json` file for Learnosity's [API authentication][1]. You'll want the `consumerKey` and `consumerSecret`
1.  Add values to `secrets.json` for `organizationId`, `consumerKey` and `consumerSecret`, and `domain`. **Don't commit the resulting file to version control.**

    Example `secrets.json`:

    ```json
    {
      "organizationId": foo,
      "domain": "localhost",
      "consumerKey": "",
      "consumerSecret": ""
    }
    ```

    Our Python script can then load that JSON file and use its contents when issuing requests. You don't _have_ to call your file `secrets.json`; you can call it whatever you like. Just pass your filename as the `credentials` parameter to the script.

1.  Run the Python script to grab learnosity data. Below are some examples

    ```bash
    # Get a specific question and print to stdout
    python get-data-from-learnosity.py \
        --credentials secrets.json \
        --endpoint questions \
        --reference 8c375ea6-4000-40fa-bb5b-4d7a64463284\

    # Get a specific activity and save the response JSON
    python get-data-from-learnosity.py \
        --credentials file-we-definitely-didnt-commit-to-git.json \
        --endpoint activities \
        --reference AGA_FL20E_LRN_G11U2M03L03_0005 \
        > response.json

    # Get 100 items
    python get-data-from-learnosity.py \
        --credentials secrets.json \
        --endpoint items \
        --limit 100 \
        > response.json
    ```

1.  See `--help` for script usage information

    ```bash
    python get-data-from-learnosity.py --help
    ```

[1]: https://docs.learnosity.com/assessment/questions/security
