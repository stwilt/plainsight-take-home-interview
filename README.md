# User aggregation

The purpose of this program is to aggregate user activities into a nested JSON format for downstream processing.

## Running
To run the script, first, make sure you're in your preferred [virtual environment](https://docs.python.org/3/tutorial/venv.html). Once you're all set up in a place where you're comfortable installing your dependencies, run:

```sh
pip install requirements.txt
```

This will install [pola.rs](https://pola.rs/) for data munging and [fire](https://github.com/google/python-fire) for CLI. 

To run the user aggregator, first, export the user activity as a CSV table. The input table should have the column headers:
- `User ID`
- `Random String`
- `Count`
- `TimeStamp` (note the camel case)

Save the file and take note of the path. Then, run:

```sh
# the activity file path defaults to ./user_activities.csv
python aggregate_users.py /path/to/your/user_activities.csv > output.json
```

Assuming the data is well-formed and all worked as intended, this will dump the aggregates to a file named `output.json`. Note that no validation (e.g., of timestamps) is performed on this data except to ensure that it is valid CSV and has the expected column headers.

Example output:
```json
{
    "User ID": "user_0077",
    "ip_addresses": [
        "231.66.126.240",
        "16.240.110.220",
        "166.180.150.132",
        "14.29.10.141",
        "15.225.56.234",
        "48.76.26.131",
        "173.15.117.130",
        "47.76.50.160",
        "207.187.141.191",
        "179.72.96.25",
        "65.114.72.191"
    ],
    "activities": [
        "Purchase",
        "Login",
        "Purchase",
        "Logout",
        "Login",
        "Login",
        "Login",
        "View",
        "View",
        "Logout",
        "Login"
    ],
    "timestamps": [
        "2023-08-30 3:39:31",
        "2024-02-14 8:03:20",
        "2023-06-04 9:48:05",
        "2024-04-01 3:23:13",
        "2023-07-18 23:16:40",
        "2023-08-26 9:18:51",
        "2023-06-21 19:43:12",
        "2023-12-04 2:56:53",
        "2023-06-07 19:59:44",
        "2024-01-06 9:01:10",
        "2023-07-17 15:40:27"
    ],
    "total_count": 65
}
```