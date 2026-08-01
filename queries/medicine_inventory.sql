-- =====================================================
-- TABLE : medicine_inventory
-- =====================================================

CREATE TABLE IF NOT EXISTS medicine_inventory (

    -- =================================================
    -- Primary Key
    -- =================================================

    id UUID PRIMARY KEY
        DEFAULT gen_random_uuid(),

    -- =================================================
    -- Foreign Key
    -- =================================================

    medicine_id UUID NOT NULL,

    -- =================================================
    -- Inventory Details
    -- =================================================

    batch_number TEXT NOT NULL
        CHECK (length(trim(batch_number)) > 0),

    expiry_date DATE NOT NULL,

    quantity_in_stock INTEGER NOT NULL
        DEFAULT 0
        CHECK (quantity_in_stock >= 0),

    unit_price NUMERIC(10,2) NOT NULL
        CHECK (unit_price >= 0),

    -- =================================================
    -- Audit Columns
    -- =================================================

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL
        DEFAULT NOW(),

    -- =================================================
    -- Foreign Key Constraint
    -- =================================================

    CONSTRAINT fk_inventory_medicine
        FOREIGN KEY (medicine_id)
        REFERENCES medicines(id)
        ON DELETE CASCADE,

    -- =================================================
    -- Prevent Duplicate Batch Entries
    -- =================================================

    CONSTRAINT uq_inventory_batch
        UNIQUE (
            medicine_id,
            batch_number
        )

);

-- =====================================================
-- Indexes
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_inventory_medicine
ON medicine_inventory(medicine_id);

CREATE INDEX IF NOT EXISTS idx_inventory_batch
ON medicine_inventory(batch_number);

CREATE INDEX IF NOT EXISTS idx_inventory_expiry
ON medicine_inventory(expiry_date);

-- =====================================================
-- Trigger : Auto-update updated_at
-- =====================================================

DROP TRIGGER IF EXISTS update_inventory_timestamp
ON medicine_inventory;

CREATE TRIGGER update_inventory_timestamp

BEFORE UPDATE
ON medicine_inventory

FOR EACH ROW

EXECUTE FUNCTION update_updated_at_column();

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
WHERE tc.table_name = 'medicine_inventory'
AND tc.constraint_type = 'FOREIGN KEY';

-- =====================================================
-- Verify Trigger
-- =====================================================

SELECT trigger_name
FROM information_schema.triggers
WHERE event_object_table = 'medicine_inventory';