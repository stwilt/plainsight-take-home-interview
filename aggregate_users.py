import json
import sys

import fire
import polars as pl


def dump_user_aggregates(activity_table_path="user_activities.csv"):
    "Write aggregate user activities as a JSON blob to stdout."
    # Lookup table mapping input column names to their output aggregate
    # names: pluralized and snake_cased
    agg_names = {
        "Activity": "activities",
        "TimeStamp": "timestamps",
        "IP Address": "ip_addresses",
        "Count": "total_count",
    }
    aggregates = (
        pl.scan_csv(
            activity_table_path,
            infer_schema_length=0,
            schema={
                "User ID": pl.String,
                "IP Address": pl.String,
                "TimeStamp": pl.String,
                "Count": pl.Int64,
                "Activity": pl.String,
                "Random String": pl.String,
            },
        )
        .select(
            pl.all().first().over("Random String", "User ID")
        )  # skip duplicate nonce
        .group_by("User ID")
        .agg(
            # Nested lists:
            pl.col("IP Address"),  # IPs per event
            pl.col("Activity"),  # Activities per event
            pl.col("TimeStamp"),  # Timestamps per event
            # Total count:
            pl.col("Count").sum(),
        )
        .rename(agg_names)
    )
    msg = None
    try:
        aggregates = aggregates.collect()
    except pl.ComputeError as err:
        msg = ".\n".join(str(err).split("\n\n")[:2])
    except Exception as err:
        msg = str(err)
    if msg is not None:
        raise RuntimeError(f"parse {activity_table_path}: {msg}")
    # The resulting table is in row-wise format with user ID as a record key: we
    # need these to be the dict keys in the output, instead
    uids = aggregates.select("User ID").to_series()
    # NOTE: could be possible to keep peak mem lower for large input by processing
    # the records in fixed size batches (see pl.DataFrame.iter_slices). HOWEVER,
    # this would not be necessary if not for the serialization format (ndjson is
    # usually fine?)
    rows = aggregates.drop("User ID").to_dicts()
    output = dict(zip(uids, rows))
    json.dump(output, sys.stdout)


if __name__ == "__main__":
    fire.Fire(dump_user_aggregates)
