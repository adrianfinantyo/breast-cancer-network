import calendar
import time

from diseases import diseases_cleaning
import utils
import config
import os
import pandas as pd

logger = utils.logger()


def main():
    logger.info("Starting", "Starting data cleaning")
    csv_file = os.path.join(config.PROJECT_ROOT, "data",
                            "1676917147-diseases-17607.csv")

    try:
        df = pd.read_csv(csv_file)
        df = diseases_cleaning(df)

        ts = calendar.timegm(time.gmtime())
        num_dis = df.shape[0]
        file_name = "{}-diseases-unique-{}.csv".format(ts, num_dis)
        df.to_csv(os.path.join(config.PROJECT_ROOT,
                  "data", file_name), index=False)
    except Exception as e:
        logger.error("Error", "Error while cleaning diseases data")
        logger.error("Error", e)
    finally:
        logger.info("Finished", "Job finished")

    exit(1)


if __name__ == "__main__":
    main()
