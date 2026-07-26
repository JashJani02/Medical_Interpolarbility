-- medical record table

-- =====================================================
-- Generic Trigger Function
-- Run ONLY ONCE for the entire database
-- =====================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()

RETURNS TRIGGER AS $$

BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;

$$ LANGUAGE plpgsql;


-- =====================================================
-- TABLE : medical_records
-- =====================================================

CREATE TABLE IF NOT EXISTS medical_records (

    -- Primary Key
    id UUID PRIMARY KEY
        DEFAULT gen_random_uuid(),

    -- Foreign Keys
    appointment_id UUID NOT NULL,

    patient_id UUID NOT NULL,

    doctor_id UUID NOT NULL,

    -- Medical Details
    diagnosis TEXT NOT NULL
        CHECK (length(trim(diagnosis)) > 0),

    symptoms TEXT,

    treatment TEXT,

    notes TEXT,

    -- Follow-up Information
    follow_up_required BOOLEAN NOT NULL
        DEFAULT FALSE,

    follow_up_date DATE,

    -- Audit Columns
    created_at TIMESTAMPTZ NOT NULL
        DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL
        DEFAULT NOW(),

    -- =================================================
    -- Foreign Key Constraints
    -- =================================================

    CONSTRAINT fk_medical_record_appointment
        FOREIGN KEY (appointment_id)
        REFERENCES appointments(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_medical_record_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_medical_record_doctor
        FOREIGN KEY (doctor_id)
        REFERENCES doctors(id)
        ON DELETE CASCADE,

    -- =================================================
    -- Validation Constraints
    -- =================================================

    CONSTRAINT chk_follow_up_date
        CHECK (
            follow_up_required = FALSE
            OR follow_up_date IS NOT NULL
        )

);


-- =====================================================
-- Indexes
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_medical_records_patient
ON medical_records(patient_id);

CREATE INDEX IF NOT EXISTS idx_medical_records_doctor
ON medical_records(doctor_id);

CREATE INDEX IF NOT EXISTS idx_medical_records_appointment
ON medical_records(appointment_id);

CREATE INDEX IF NOT EXISTS idx_medical_records_created_at
ON medical_records(created_at);


-- =====================================================
-- Trigger : Auto-update updated_at
-- =====================================================

DROP TRIGGER IF EXISTS update_medical_record_timestamp
ON medical_records;

CREATE TRIGGER update_medical_record_timestamp

BEFORE UPDATE
ON medical_records

FOR EACH ROW

EXECUTE FUNCTION update_updated_at_column();

-- to check foreign keys
SELECT
    tc.constraint_name,
    kcu.column_name,
    ccu.table_name AS references_table,
    ccu.column_name AS references_column
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.table_name = 'medical_records'
AND tc.constraint_type = 'FOREIGN KEY';

-- verify exsistance of trigger
SELECT trigger_name
FROM information_schema.triggers
WHERE event_object_table = 'medical_records';

