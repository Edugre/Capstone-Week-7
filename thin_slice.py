import csv
import platform
import time
from collections import defaultdict


def load_patients(filename):
    records = []

    with open(filename, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            records.append({
                "patient_id": row["patient_id"],
                "zip_code": row["zip_code"],
                "screened": int(row["screened"]),
                "referred": int(row["referred"])
            })

    return records


def build_report(records):
    report = defaultdict(lambda: {
        "screenings": 0,
        "referrals": 0
    })

    for record in records:
        zip_code = record["zip_code"]
        report[zip_code]["screenings"] += record["screened"]
        report[zip_code]["referrals"] += record["referred"]

    return dict(report)


def load_expected(filename):
    expected = {}

    with open(filename, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            expected[row["zip_code"]] = {
                "screenings": int(row["screenings"]),
                "referrals": int(row["referrals"])
            }

    return expected


def compare(actual, expected):
    matched = 0
    total = 0

    for zip_code, expected_values in expected.items():
        for field in ("screenings", "referrals"):
            total += 1

            actual_value = actual.get(zip_code, {}).get(field)
            expected_value = expected_values[field]

            if actual_value == expected_value:
                matched += 1

            print(
                f"{zip_code} {field}: "
                f"expected={expected_value}, actual={actual_value}"
            )

    return matched, total


test_cases = [
    ("Test Case 1", "patient_fixture.csv", "expected_report.csv"),
    ("Test Case 2", "patient_data_2.csv", "expected_report_2.csv")
]

for name, patient_file, expected_file in test_cases:
    print(f"\n========== {name} ==========")

    start = time.perf_counter()

    patients = load_patients(patient_file)
    actual_report = build_report(patients)
    expected_report = load_expected(expected_file)

    matched, total = compare(actual_report, expected_report)

    elapsed_ms = (time.perf_counter() - start) * 1000
    accuracy = matched / total * 100

    print("\n--- MEASUREMENT ---")
    print(f"Patient records: {len(patients)}")
    print(f"Values matched: {matched}/{total}")
    print(f"Report accuracy: {accuracy:.1f}%")
    print(f"Runtime: {elapsed_ms:.3f} ms")
    print(f"Python: {platform.python_version()}")
    print(f"Machine: {platform.platform()}")