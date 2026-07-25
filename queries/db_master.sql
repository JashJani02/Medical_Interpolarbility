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



-- doctor table
CREATE TABLE doctors (

    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    doctor_name TEXT NOT NULL,

    doctor_phone TEXT NOT NULL UNIQUE,

    hospital_address TEXT NOT NULL,

    specialization TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()

);

-- populate the doctors table with sample data
INSERT INTO doctors (
    doctor_name,
    doctor_phone,
    hospital_address,
    specialization
)
VALUES
(
    'Dr. Rajesh Shah',
    '+919876543210',
    'Apollo Hospital, Ahmedabad, Gujarat',
    'Cardiologist'
),
(
    'Dr. Priya Patel',
    '+919876543211',
    'Sterling Hospital, Ahmedabad, Gujarat',
    'Dermatologist'
),
(
    'Dr. Amit Kumar',
    '+919876543212',
    'Civil Hospital, Ahmedabad, Gujarat',
    'Neurologist'
),
(
    'Dr. Neha Sharma',
    '+919876543213',
    'KD Hospital, Ahmedabad, Gujarat',
    'Pediatrician'
),
(
    'Dr. Vivek Mehta',
    '+919876543214',
    'Zydus Hospital, Ahmedabad, Gujarat',
    'Orthopedic'
),
(
    'Dr. Rina Desai',
    '+919876543215',
    'Shalby Hospital, Ahmedabad, Gujarat',
    'General Physician'
),
(
    'Dr. Arjun Joshi',
    '+919876543216',
    'HCG Cancer Centre, Ahmedabad, Gujarat',
    'Oncologist'
),
(
    'Dr. Kavita Rao',
    '+919876543217',
    'CIMS Hospital, Ahmedabad, Gujarat',
    'Psychiatrist'
),
(
    'Dr. Harsh Trivedi',
    '+919876543218',
    'Narayana Multispeciality Hospital, Ahmedabad, Gujarat',
    'ENT'
),
(
    'Dr. Sneha Iyer',
    '+919876543219',
    'Wockhardt Hospital, Rajkot, Gujarat',
    'Gynecologist'
),
(
    'Dr. Nikhil Soni',
    '+919876543220',
    'Sunshine Global Hospital, Vadodara, Gujarat',
    'Radiologist'
),
(
    'Dr. Meera Nair',
    '+919876543221',
    'SAL Hospital, Ahmedabad, Gujarat',
    'Ophthalmologist'
),
(
    'Dr. Rohit Kapoor',
    '+919876543222',
    'UN Mehta Institute of Cardiology, Ahmedabad, Gujarat',
    'Cardiologist'
),
(
    'Dr. Asha Menon',
    '+919876543223',
    'Care Institute of Medical Sciences (CIMS), Ahmedabad, Gujarat',
    'Dermatologist'
),
(
    'Dr. Karan Malhotra',
    '+919876543224',
    'Civil Hospital, Surat, Gujarat',
    'Dentist'
),
(    'Dr. Anjali Joshi',
    '+919876543235',
    'Ayush Wellness Centre, Ahmedabad, Gujarat',
    'Ayurveda'
),
(
    'Dr. Rakesh Verma',
    '+919876543236',
    'National Homeopathy Clinic, Vadodara, Gujarat',
    'Homeopathy'
),
(
    'Dr. Mehul Bhatt',
    '+919876543237',
    'Siddha Medical Centre, Chennai, Tamil Nadu',
    'Siddha'
),
(
    'Dr. Pooja Iyer',
    '+919876543238',
    'Naturopathy & Yoga Institute, Bengaluru, Karnataka',
    'Naturopathy'
),
(
    'Dr. Sanjay Kulkarni',
    '+919876543239',
    'Integrated Healthcare Centre, Pune, Maharashtra',
    'Integrative Medicine'
);

-- doctor_availability table
CREATE TABLE doctor_availability (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    doctor_id UUID NOT NULL,

    weekday TEXT NOT NULL,

    start_time TIME NOT NULL,

    end_time TIME NOT NULL,

    is_available BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT fk_doctor
        FOREIGN KEY (doctor_id)
        REFERENCES doctors(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_weekday
        CHECK (
            weekday IN (
                'Monday',
                'Tuesday',
                'Wednesday',
                'Thursday',
                'Friday',
                'Saturday',
                'Sunday'
            )
        ),

    CONSTRAINT chk_time
        CHECK (start_time < end_time)

);

CREATE INDEX idx_doctor_availability_doctor
ON doctor_availability(doctor_id);

INSERT INTO doctor_availability
(
    doctor_id,
    weekday,
    start_time,
    end_time,
    is_available
)

SELECT
    d.id,
    s.weekday,
    s.start_time,
    s.end_time,
    TRUE

FROM doctors d

JOIN (

    /* Morning Shift */
    SELECT
        'Morning' AS shift,
        weekday,
        start_time,
        end_time
    FROM (
        VALUES
        ('Monday',    TIME '08:00', TIME '16:00'),
        ('Tuesday',   TIME '08:00', TIME '16:00'),
        ('Wednesday', TIME '08:00', TIME '16:00'),
        ('Thursday',  TIME '08:00', TIME '16:00'),
        ('Friday',    TIME '08:00', TIME '16:00'),
        ('Saturday',  TIME '09:00', TIME '13:00')
    ) x(weekday,start_time,end_time)

    UNION ALL

    /* General Shift */

    SELECT
        'General',
        weekday,
        start_time,
        end_time
    FROM (
        VALUES
        ('Monday',    TIME '09:00', TIME '17:00'),
        ('Tuesday',   TIME '09:00', TIME '17:00'),
        ('Wednesday', TIME '09:00', TIME '17:00'),
        ('Thursday',  TIME '09:00', TIME '17:00'),
        ('Friday',    TIME '09:00', TIME '17:00'),
        ('Saturday',  TIME '09:00', TIME '13:00'),
        ('Sunday',    TIME '10:00', TIME '14:00')
    ) x(weekday,start_time,end_time)

    UNION ALL

    /* Evening Shift */

    SELECT
        'Evening',
        weekday,
        start_time,
        end_time
    FROM (
        VALUES
        ('Monday',    TIME '12:00', TIME '20:00'),
        ('Tuesday',   TIME '12:00', TIME '20:00'),
        ('Wednesday', TIME '12:00', TIME '20:00'),
        ('Thursday',  TIME '12:00', TIME '20:00'),
        ('Friday',    TIME '12:00', TIME '20:00'),
        ('Saturday',  TIME '13:00', TIME '17:00')
    ) x(weekday,start_time,end_time)

) s

ON s.shift =

CASE

    WHEN d.specialization IN
    (
        'Cardiologist',
        'Neurologist',
        'Radiologist',
        'Ayurveda',
        'Homeopathy',
        'Siddha',
        'Naturopathy'
    )

    THEN 'Morning'

    WHEN d.specialization IN
    (
        'General Physician',
        'Dermatologist',
        'Pediatrician',
        'ENT',
        'Dentist',
        'Ophthalmologist',
        'Gynecologist',
        'Integrative Medicine'
    )

    THEN 'General'

    ELSE 'Evening'

END;

SELECT
    d.doctor_name,
    d.specialization,
    da.weekday,
    da.start_time,
    da.end_time
FROM doctor_availability da
JOIN doctors d
ON da.doctor_id = d.id
ORDER BY
    d.doctor_name,
    CASE da.weekday
        WHEN 'Monday' THEN 1
        WHEN 'Tuesday' THEN 2
        WHEN 'Wednesday' THEN 3
        WHEN 'Thursday' THEN 4
        WHEN 'Friday' THEN 5
        WHEN 'Saturday' THEN 6
        WHEN 'Sunday' THEN 7
    END;


-- appointments table
CREATE TABLE appointments (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    patient_id UUID NOT NULL,

    doctor_id UUID NOT NULL,

    appointment_date DATE NOT NULL,

    appointment_time TIME NOT NULL,

    status TEXT NOT NULL DEFAULT 'Pending',

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT fk_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_doctor
        FOREIGN KEY (doctor_id)
        REFERENCES doctors(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_status
        CHECK (
            status IN (
                'Pending',
                'Confirmed',
                'Cancelled',
                'Completed'
            )
        )

);

CREATE INDEX idx_appointments_patient
ON appointments(patient_id);

CREATE INDEX idx_appointments_doctor
ON appointments(doctor_id);

CREATE INDEX idx_appointments_date
ON appointments(appointment_date);