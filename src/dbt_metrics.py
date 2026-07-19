import json
from pathlib import Path


DBT_RESULTS = Path(
    "/opt/airflow/dbt_project/healthcare_dbt/target/run_results.json"
)


def get_dbt_metrics():
    """
    Parse dbt run_results.json and return execution metrics.
    """

    if not DBT_RESULTS.exists():
        return {
            "dbt_models": 0,
            "tests_total": 0,
            "tests_passed": 0,
            "tests_failed": 0,
        }

    with open(DBT_RESULTS, "r") as f:
        results = json.load(f)

    dbt_models = 0
    tests_total = 0
    tests_passed = 0
    tests_failed = 0

    for result in results["results"]:

        resource_type = result["unique_id"].split(".")[0]

        if resource_type == "model":
            dbt_models += 1

        elif resource_type == "test":

            tests_total += 1

            if result["status"] == "pass":
                tests_passed += 1
            else:
                tests_failed += 1

    return {
        "dbt_models": dbt_models,
        "tests_total": tests_total,
        "tests_passed": tests_passed,
        "tests_failed": tests_failed,
    }