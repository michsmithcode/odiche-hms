
PERMISSIONS = [
    ("can_access_dashboard", "Access hospital dashboard"),
    ("can_manage_hospital_settings", "Manage hospital settings"),
    ("can_manage_roles", "Create/update/delete roles"),
    ("can_manage_permissions", "Create/update/delete permissions"),
    ("can_view_audit_logs", "View audit logs"),
    ("can_manage_users", "Create/update/delete users"),
    ("can_deactivate_users", "Deactivate users"),
    ("can_reset_passwords", "Reset user passwords"),

    # Patients
    ("can_add_patient", "Add new patient"),
    ("can_edit_patient", "Edit patient"),
    ("can_view_patient", "View patient"),
    ("can_delete_patient", "Delete patient"),
    ("can_view_patient_history", "View patient history"),
    ("can_view_own_record", "Patient can view own record"),

    # Doctor
    ("can_create_consultation", "Create consultation"),
    ("can_edit_consultation", "Edit consultation"),
    ("can_view_consultation", "View consultation"),
    ("can_create_diagnosis", "Create diagnosis"),
    ("can_prescribe_medication", "Prescribe medication"),
    ("can_book_appointment", "Book appointment"),

    # Nurse
    ("can_record_vitals", "Record patient vitals"),
    ("can_assign_nurse_to_patient", "Assign nurse to patient"),
    ("can_update_patient_status", "Update patient status"),

    # Pharmacy
    ("can_add_drug", "Add drug"),
    ("can_edit_drug", "Edit drug"),
    ("can_view_drug", "View drug"),
    ("can_manage_stock", "Manage drug stock"),
    ("can_process_prescriptions", "Process prescriptions"),
    ("can_dispense_drugs", "Dispense drugs"),
    ("can_view_expired_drugs", "View expired drugs"),

    # Pharmacy cashier
    ("can_record_payment", "Record payments"),
    ("can_view_invoice", "View invoices"),

    # Lab
    ("can_add_lab_test", "Add lab test"),
    ("can_upload_lab_result", "Upload lab result"),
    ("can_view_lab_result", "View lab result"),

    # Reception
    ("can_register_patient", "Register patient"),
    ("can_update_patient_contact", "Update patient contact"),
    ("can_check_in_patient", "Check in patient"),

    # Billing
    ("can_create_invoice", "Create invoice"),
    ("can_refund_payment", "Refund payments"),
    ("can_view_financial_reports", "View financial reports"),
]

ROLES = [
    "Main_Admin",
    "Hospital_Admin",
    "Doctor",
    "Nurse",
    "Pharmacist",
    "Pharmacy_Cashier",
    "Lab Technician",
    "Receptionist",
    "Accountant",
    "Patient",
]

ROLE_PERMISSION_MAP = {
    "Main_Admin": ["ALL"],

    "Hospital_Admin": [
        "can_access_dashboard",
        "can_manage_hospital_settings",
        "can_manage_roles",
        "can_manage_permissions",
        "can_view_audit_logs",
        "can_manage_users",
        "can_deactivate_users",
        "can_reset_passwords",
        "can_view_patient",
        "can_view_patient_history",
        "can_view_financial_reports",
    ],

    "Doctor": [
        "can_create_consultation",
        "can_edit_consultation",
        "can_view_consultation",
        "can_create_diagnosis",
        "can_prescribe_medication",
        "can_book_appointment",
        "can_view_patient",
        "can_view_patient_history",
        "can_view_lab_result",
    ],

    "Nurse": [
        "can_record_vitals",
        "can_assign_nurse_to_patient",
        "can_update_patient_status",
        "can_view_patient",
        "can_view_patient_history",
        "can_assist_doctor",
    ],

    "Pharmacist": [
        "can_add_drug",
        "can_edit_drug",
        "can_view_drug",
        "can_manage_stock",
        "can_process_prescriptions",
        "can_dispense_drugs",
        "can_view_expired_drugs",
    ],

    "Pharmacy_Cashier": [
        "can_view_drug",
        "can_process_prescriptions",
        "can_record_payment",
        "can_view_invoice",
    ],

    "Lab Technician": [
        "can_add_lab_test",
        "can_upload_lab_result",
        "can_view_lab_result",
    ],

    "Receptionist": [
        "can_register_patient",
        "can_update_patient_contact",
        "can_check_in_patient",
    ],

    "Accountant": [
        "can_create_invoice",
        "can_refund_payment",
        "can_view_invoice",
        "can_record_payment",
        "can_view_financial_reports",
    ],

    "Patient": [
        "can_view_own_record",
    ],
}



