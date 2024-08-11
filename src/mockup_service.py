import concurrent.futures
import logging
import time

import numpy as np
import pandas as pd
from tqdm import tqdm

from src.logger import logger_dpf
from src.xi_corr import XiCorr


def main():
    # Set up logging
    logger = logger_dpf()

    # Set variables
    target_col = "Electric Vehicles Revenue"
    date_col = "Calendar Date"
    np.random.seed(42)

    # Load data
    logger.log(logging.INFO, "\nLoading data...")

    df = pd.read_json("src/sample_data/car_sales_revenue.json")
    df = df[[date_col, target_col]]
    logger.log(logging.INFO, f"\nData loaded successfully. Sample: {df.head()}")

    external_data = pd.read_csv("src/sample_data/fred_monthly.csv")
    logger.log(
        logging.INFO,
        f"\nExternal data loaded successfully. Sample: {external_data.head()}\n",
    )

    features = external_data.drop(columns=[date_col]).columns.to_list()

    # Initialize XiCorr class
    xicorr = XiCorr(df, target_col, date_col, external_data)

    # Compute XiCorr
    start_time = time.time()
    completed_tasks = 0
    logger.log(logging.INFO, "\nComputing XiCorr...")
    with concurrent.futures.ProcessPoolExecutor(max_workers=4, initializer=logger_dpf) as executor:
        # res = list(executor.map(xicorr.compute_xicorr, features))
        futures = [executor.submit(xicorr.compute_xicorr, feature) for feature in features]

        res = []
        for future in concurrent.futures.as_completed(futures):
            completed_tasks += 1
            logger.log(logging.INFO, f"Completed {completed_tasks}/{len(features)}")
            res.append(future.result())


        df = pd.DataFrame(res, columns=["Feature", "Score"])
        logger.log(
            logging.INFO, f"\n\nXiCorr computed successfully. Sample\n: {df.head()}"
        )
    logger.log(
        logging.INFO,
        f"\n\nProcessed {len(features)} features in: {time.time() - start_time:.2f} seconds",
    )

    return df.to_dict(orient="records")


if __name__ == "__main__":
    main()
