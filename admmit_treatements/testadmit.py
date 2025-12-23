"""
18/12

{
    "message": "Patient admitted successfully",
    "admission": {
        "id": 2,
        "patient": 2,
        "patient_display": "testpatient2 testpatient2 - REG/2025/28364",
        "admitted_on": "2025-12-18T11:38:59.443948+01:00",
        "expected_discharge_date": "2025-12-22",
        "discharged_on": null,
        "ward": 1,
        "ward_name": "Men Ward",
        "room_number": "RM002",
        "bed": 1,
        "attending_doctor": "b4044b45-f9b3-4088-9031-bbe61f96d756",
        "doctor_display": "Dr. test",
        "diagnosis": "Appendix Surgery",
        "status": "admitted",
        "notes": "The condition is more criteical and requires urgent attention"
    }
}
{
    "message": "Patient admitted successfully",
    "admission": {
        "id": 1,
        "patient": 1,
        "patient_display": "testpatient testpatient - REG/2025/15116",
        "admitted_on": "2025-12-17T21:07:18.037403+01:00",
        "expected_discharge_date": "2025-12-26",
        "discharged_on": null,
        "ward": 1,
        "ward_name": "Men Ward",
        "room_number": "RM001",
        "attending_doctor": "b4044b45-f9b3-4088-9031-bbe61f96d756",
        "doctor_display": "Dr. test",
        "diagnosis": "Ulcer",
        "status": "admitted",
        "notes": "The condition is more criteical and requires urgent attention"
    }
}
treatement2

{
    "message": "Treatment added successfully",
    "treatment": {
        "id": 7,
        "admission": 2,
        "admission_display": "testpatient2 testpatient2",
        "date": "2025-12-18T11:48:04.770137+01:00",
        "doctor": "b4044b45-f9b3-4088-9031-bbe61f96d756",
        "doctor_name": "testdoctor@gmail.com",
        "description": "Appendix Surgery",
        "procedure_name": "30cl of med Surgery be injected immediateley after released from the theater",
        "medication_prescribed": "As directed by the doctor",
        "notes": "Procedure listed and verified by the doctor"
    }
}
Treatment
{{
    "message": "Treatment added successfully",
    "treatment": {
        "id": 2,
        "admission": 1,
        "admission_display": "testpatient testpatient",
        "date": "2025-12-17T21:35:15.226514+01:00",
        "doctor": "3735abf1-8b17-40ed-9528-170bb6571259",
        "doctor_name": "admin@gmail.com",
        "description": "Ulcer tab, yesdtide",
        "procedure_name": "30cl of ulcertab should be given each daily",
        "medication_prescribed": "ALL",
        "notes": "Procedure verified by the doctor"
    }
    }
}

"""