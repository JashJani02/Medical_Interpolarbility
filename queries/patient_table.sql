-- rename Patients_db to patients
ALTER TABLE "Patient_db"
RENAME TO patients;

ALTER TABLE patients
RENAME COLUMN "Patient_Name" TO patient_name;

ALTER TABLE patients
RENAME COLUMN "Phone_Number" TO phone_number;

ALTER TABLE patients
RENAME COLUMN "Blood_Group" TO blood_group;

ALTER TABLE patients
ADD COLUMN dob DATE;

ALTER TABLE patients
ADD COLUMN height_cm NUMERIC(5,2);

ALTER TABLE patients
ADD COLUMN weight_kg NUMERIC(5,2);

ALTER TABLE patients
ADD COLUMN allergies JSONB DEFAULT '[]'::jsonb;

ALTER TABLE patients
ADD COLUMN updated_at TIMESTAMPTZ DEFAULT now();

ALTER TABLE patients
ALTER COLUMN patient_name SET NOT NULL;

ALTER TABLE patients
ALTER COLUMN phone_number SET NOT NULL;

ALTER TABLE patients
ALTER COLUMN blood_group SET NOT NULL;

ALTER TABLE patients
ALTER COLUMN created_at SET NOT NULL;

ALTER TABLE patients
ADD CONSTRAINT patients_phone_number_unique
UNIQUE (phone_number);

ALTER TABLE patients
ADD CONSTRAINT patients_blood_group_check
CHECK (
    blood_group IN (
        'A+','A-',
        'B+','B-',
        'AB+','AB-',
        'O+','O-'
    )
);

-- populate the dob, height_cm, weight_kg, and allergies columns with sample data
UPDATE patients
SET dob = DATE '1998-01-01' + FLOOR(RANDOM() * 8000)::INT
WHERE dob IS NULL;

UPDATE patients
SET height_cm = ROUND((150 + RANDOM() * 40)::numeric, 2)
WHERE height_cm IS NULL;

UPDATE patients
SET weight_kg = ROUND((45 + RANDOM() * 55)::numeric, 2)
WHERE weight_kg IS NULL;

UPDATE patients
SET allergies =
CASE FLOOR(RANDOM() * 20)

    WHEN 0  THEN '["Dust"]'::jsonb
    WHEN 1  THEN '["Pollen"]'::jsonb
    WHEN 2  THEN '["Penicillin"]'::jsonb
    WHEN 3  THEN '["Peanuts"]'::jsonb
    WHEN 4  THEN '["Dust","Pollen"]'::jsonb
    WHEN 5  THEN '["Penicillin","Peanuts"]'::jsonb

    ELSE '[]'::jsonb

END
WHERE allergies IS NULL
   OR allergies = '[]'::jsonb;


ALTER TABLE patients
ALTER COLUMN dob SET NOT NULL;

UPDATE patients
SET updated_at = now()
WHERE updated_at IS NULL;

ALTER TABLE patients
ALTER COLUMN updated_at SET NOT NULL;

-- view to display patient age
CREATE OR REPLACE VIEW patient_details AS
SELECT
    id,
    patient_name,
    phone_number,
    blood_group,
    dob,
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, dob))::INT AS age,
    height_cm,
    weight_kg,
    allergies,
    created_at,
    updated_at
FROM patients;

-- run below query to see the view
SELECT * FROM patient_details;