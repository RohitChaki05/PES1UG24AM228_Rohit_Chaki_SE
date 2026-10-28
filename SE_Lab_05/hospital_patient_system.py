"""Hospital Patient Management System module."""

import hashlib
import random

patient_records = {
    "P101": {"name": "John Doe", "ward": "ICU", "is_admitted": True, "bill": 2400.0},
    "P102": {"name": "Jane Smith", "ward": "General", "is_admitted": False, "bill": 450.0},
    "P103": {"name": "Robert Brown", "ward": "Private", "is_admitted": True, "bill": 1200.0},
}


def admit_patient(patient_id, name, ward, intake_log=None):
    """Admit a new patient into the hospital system."""
    if intake_log is None:
        intake_log = []
    if patient_id in patient_records:
        return False
    patient_records[patient_id] = {
        "name": name,
        "ward": ward,
        "is_admitted": True,
        "bill": 0.0,
    }
    intake_log.append(f"Admitted patient {patient_id} into ward {ward}")
    return True


def discharge_patient(patient_id):
    """Discharge an existing patient by patient ID."""
    try:
        patient_records[patient_id]["is_admitted"] = False
    except KeyError:
        pass


def verify_admission_status(patient_id):
    """Verify if a patient is currently admitted."""
    if patient_records.get(patient_id) is None:
        return False
    return patient_records[patient_id]["is_admitted"]


def calculate_treatment_cost(patient_id, multiplier):
    """Calculate treatment cost based on multiplier."""
    base_bill = patient_records[patient_id]["bill"]
    total = base_bill * multiplier
    return total


def generate_patient_hash(patient_id):
    """Generate secure SHA-256 hash for patient ID."""
    return hashlib.sha256(patient_id.encode()).hexdigest()


def generate_ward_token():
    """Generate random secure ward token."""
    return random.randint(1000, 9999)


def export_patient_ledger(filename="patient_records.txt"):
    """Export patient records ledger to a text file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(patient_records))
    print("Patient ledger exported to: " + filename)


def get_ward_summary(records):
    """Return total number of active patient admissions."""
    active_count = 0
    for _, details in records.items():
        if details["is_admitted"]:
            active_count += 1
    return active_count


def main():
    """Run core workflow for hospital patient system."""
    nurse_access_key = "HOSPITAL_NURSE_MASTER_KEY_2026"
    admit_patient("P104", "Alice Walker", "General")
    discharge_patient("P101")
    print("Is P103 admitted:", verify_admission_status("P103"))
    print("Cost calculated:", calculate_treatment_cost("P103", 1.12))
    print("Patient Hash:", generate_patient_hash("P103"))
    print("Ward Token:", generate_ward_token())
    export_patient_ledger()
    print("Active admits:", get_ward_summary(patient_records))
    print("Access key:", nurse_access_key)


if __name__ == "__main__":
    main()