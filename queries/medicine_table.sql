-- =====================================================
-- TABLE : medicines
-- =====================================================

CREATE TABLE IF NOT EXISTS medicines (

    -- =================================================
    -- Primary Key
    -- =================================================

    id UUID PRIMARY KEY
        DEFAULT gen_random_uuid(),

    -- =================================================
    -- Medicine Information
    -- =================================================

    name TEXT NOT NULL
        CHECK (length(trim(name)) > 0),

    generic_name TEXT,

    strength TEXT,

    dosage_form TEXT NOT NULL
        CHECK (
            dosage_form IN (
                'Tablet',
                'Capsule',
                'Syrup',
                'Injection',
                'Cream',
                'Ointment',
                'Drops',
                'Inhaler',
                'Suspension',
                'Powder',
                'Gel',
                'Solution',
                'Other'
            )
        ),

    manufacturer TEXT,

    description TEXT,

    -- =================================================
    -- Audit Columns
    -- =================================================

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL
        DEFAULT NOW(),

    -- =================================================
    -- Validation Constraints
    -- =================================================

    CONSTRAINT uq_medicine
        UNIQUE (
            name,
            generic_name,
            strength,
            dosage_form
        )

);

-- =====================================================
-- Indexes
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_medicines_name
ON medicines(name);

CREATE INDEX IF NOT EXISTS idx_medicines_generic_name
ON medicines(generic_name);

CREATE INDEX IF NOT EXISTS idx_medicines_dosage_form
ON medicines(dosage_form);

-- =====================================================
-- Trigger : Auto-update updated_at
-- =====================================================

DROP TRIGGER IF EXISTS update_medicine_timestamp
ON medicines;

CREATE TRIGGER update_medicine_timestamp

BEFORE UPDATE
ON medicines

FOR EACH ROW

EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- Verify Table Constraints
-- =====================================================

SELECT
    constraint_name,
    constraint_type
FROM information_schema.table_constraints
WHERE table_name = 'medicines';

-- =====================================================
-- Verify Trigger
-- =====================================================

SELECT trigger_name
FROM information_schema.triggers
WHERE event_object_table = 'medicines';