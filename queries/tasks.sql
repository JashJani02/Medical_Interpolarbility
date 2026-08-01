-- =====================================================
-- TABLE : tasks
-- =====================================================

CREATE TABLE IF NOT EXISTS tasks (

    -- =================================================
    -- Primary Key
    -- =================================================

    id UUID PRIMARY KEY
        DEFAULT gen_random_uuid(),

    -- =================================================
    -- Task Information
    -- =================================================

    title TEXT NOT NULL
        CHECK (length(trim(title)) > 0),

    assigned_to UUID NOT NULL
        REFERENCES admins(id)
        ON DELETE CASCADE,

    status TEXT NOT NULL
        DEFAULT 'In Progress'
        CHECK (
            status IN (
                'Completed',
                'In Progress',
                'Delayed'
            )
        ),

    progress INTEGER NOT NULL
        DEFAULT 0
        CHECK (
            progress >= 0
            AND progress <= 100
        ),

    start_date DATE NOT NULL,

    end_date DATE NOT NULL
        CHECK (end_date >= start_date),

    -- =================================================
    -- Audit Columns
    -- =================================================

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL
        DEFAULT NOW()

);

-- =====================================================
-- Indexes
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_tasks_assigned_to
ON tasks(assigned_to);

CREATE INDEX IF NOT EXISTS idx_tasks_status
ON tasks(status);

CREATE INDEX IF NOT EXISTS idx_tasks_start_date
ON tasks(start_date);

CREATE INDEX IF NOT EXISTS idx_tasks_end_date
ON tasks(end_date);

CREATE INDEX IF NOT EXISTS idx_tasks_created_at
ON tasks(created_at);

-- =====================================================
-- Trigger : Auto-update updated_at
-- =====================================================

DROP TRIGGER IF EXISTS update_task_timestamp
ON tasks;

CREATE TRIGGER update_task_timestamp

BEFORE UPDATE
ON tasks

FOR EACH ROW

EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- Enable Row Level Security
-- =====================================================

ALTER TABLE tasks
ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- Verify Table Constraints
-- =====================================================

SELECT
    constraint_name,
    constraint_type
FROM information_schema.table_constraints
WHERE table_name = 'tasks';

-- =====================================================
-- Verify Trigger
-- =====================================================

SELECT
    trigger_name
FROM information_schema.triggers
WHERE event_object_table = 'tasks';