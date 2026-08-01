-- =====================================================
-- TABLE : admins
-- =====================================================

CREATE TABLE IF NOT EXISTS admins (

    -- =================================================
    -- Primary Key
    -- =================================================

    id UUID PRIMARY KEY
        REFERENCES auth.users(id)
        ON DELETE CASCADE,

    -- =================================================
    -- Administrator Information
    -- =================================================

    full_name TEXT NOT NULL
        CHECK (length(trim(full_name)) > 0),

    email TEXT NOT NULL
        UNIQUE
        CHECK (length(trim(email)) > 0),

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

CREATE INDEX IF NOT EXISTS idx_admins_full_name
ON admins(full_name);

CREATE INDEX IF NOT EXISTS idx_admins_email
ON admins(email);

CREATE INDEX IF NOT EXISTS idx_admins_created_at
ON admins(created_at);

-- =====================================================
-- Trigger : Auto-update updated_at
-- =====================================================

DROP TRIGGER IF EXISTS update_admin_timestamp
ON admins;

CREATE TRIGGER update_admin_timestamp

BEFORE UPDATE
ON admins

FOR EACH ROW

EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- Enable Row Level Security
-- =====================================================

ALTER TABLE admins
ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- Verify Table Constraints
-- =====================================================

SELECT
    constraint_name,
    constraint_type
FROM information_schema.table_constraints
WHERE table_name = 'admins';

-- =====================================================
-- Verify Trigger
-- =====================================================

SELECT
    trigger_name
FROM information_schema.triggers
WHERE event_object_table = 'admins';

-- insert policy
create policy "Users can insert themselves"
on public.admins
for insert
to authenticated
with check (
    auth.uid() = id
);

-- select policy
create policy "Users can read themselves"
on public.admins
for select
to authenticated
using (
    auth.uid() = id
);

-- update policy
create policy "Users can update themselves"
on public.admins
for update
to authenticated
using (
    auth.uid() = id
)
with check (
    auth.uid() = id
);

-- delete policy
create policy "Users can delete themselves"
on public.admins
for delete
to authenticated
using (
    auth.uid() = id
);

-- policy check
SELECT policyname, cmd, qual, with_check
FROM pg_policies
WHERE tablename = 'admins';

-- number of admins
SELECT * FROM public.admins;