-- =====================================================
-- TABLE : prescriptions
-- =====================================================

CREATE TABLE IF NOT EXISTS prescriptions (

    -- =================================================
    -- Primary Key
    -- =================================================

    prescription_uuid UUID PRIMARY KEY
        DEFAULT gen_random_uuid(),

    -- =================================================
    -- Foreign Keys
    -- =================================================

    medical_record_uuid UUID NOT NULL,

    medicine_id UUID NOT NULL,

    -- =================================================
    -- Prescription Details
    -- =================================================

    dosage TEXT NOT NULL
        CHECK (length(trim(dosage)) > 0),

    frequency TEXT NOT NULL
        CHECK (length(trim(frequency)) > 0),

    duration TEXT NOT NULL
        CHECK (length(trim(duration)) > 0),

    instructions TEXT,

    prescribed_date DATE NOT NULL
        DEFAULT CURRENT_DATE,

    -- =================================================
    -- Foreign Key Constraints
    -- =================================================

    CONSTRAINT fk_prescription_medical_record
        FOREIGN KEY (medical_record_uuid)
        REFERENCES medical_records(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_prescription_medicine
        FOREIGN KEY (medicine_id)
        REFERENCES medicines(id)
        ON DELETE RESTRICT

);

-- =====================================================
-- Indexes
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_prescriptions_medical_record
ON prescriptions(medical_record_uuid);

CREATE INDEX IF NOT EXISTS idx_prescriptions_medicine
ON prescriptions(medicine_id);

CREATE INDEX IF NOT EXISTS idx_prescriptions_date
ON prescriptions(prescribed_date);

-- =====================================================
-- Verify Foreign Keys
-- =====================================================

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
WHERE tc.table_name = 'prescriptions'
AND tc.constraint_type = 'FOREIGN KEY';