"""
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