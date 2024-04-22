# User aggregation

The purpose of this program is to aggregate user activities into a nested JSON format for downstream processing.

## Running
To run the script, first, make sure you're in your preferred [virtual environment](https://docs.python.org/3/tutorial/venv.html). Once you're all set up in a place where you're comfortable installing your dependencies, run:

```sh
pip install -r requirements.txt
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
  "user_0067": {
    "ip_addresses": [
      "52.47.131.133",
      "86.69.209.81",
      "153.14.192.255",
      "14.50.224.135",
      "155.101.83.62",
      [...],
    ],
    "activities": [
      "View",
      "Logout",
      "Login",
      "Logout",
      "Purchase",
      [...],
    ],
    "timestamps": [
      "2024-02-01 2:50:32",
      "2023-11-03 5:59:47",
      "2024-03-24 4:37:31",
      "2024-03-30 1:13:27",
      "2023-07-05 22:56:32",
      [...],
    ],
    "total_count": 90
  },
  [...]
}
```