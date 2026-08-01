-- for checing the rls policy status and number of policies
SELECT
    c.relname AS table_name,
    c.relrowsecurity AS rls_enabled,
    COUNT(p.policyname) AS policy_count
FROM pg_class c
LEFT JOIN pg_policies p
ON p.tablename = c.relname
WHERE c.relkind = 'r'
AND c.relnamespace = (
    SELECT oid
    FROM pg_namespace
    WHERE nspname = 'public'
)
GROUP BY c.relname, c.relrowsecurity
ORDER BY c.relname;


-- sql script to create select, insert, update and delete policies for all available tables
DO $$
DECLARE
    tbl text;
BEGIN
    FOREACH tbl IN ARRAY ARRAY[
        'patients',
        'doctors',
        'doctor_availability',
        'medical_records',
        'medicines',
        'medicine_inventory',
        'prescriptions',
        'lab_reports',
        'tasks'
    ]
    LOOP

        IF NOT EXISTS (
            SELECT 1 FROM pg_policies
            WHERE schemaname='public'
              AND tablename=tbl
              AND policyname='Authenticated users can read ' || tbl
        ) THEN
            EXECUTE format(
                'CREATE POLICY "Authenticated users can read %s"
                 ON public.%I
                 FOR SELECT
                 TO authenticated
                 USING (true);',
                tbl, tbl
            );
        END IF;

        IF NOT EXISTS (
            SELECT 1 FROM pg_policies
            WHERE schemaname='public'
              AND tablename=tbl
              AND policyname='Authenticated users can insert ' || tbl
        ) THEN
            EXECUTE format(
                'CREATE POLICY "Authenticated users can insert %s"
                 ON public.%I
                 FOR INSERT
                 TO authenticated
                 WITH CHECK (true);',
                tbl, tbl
            );
        END IF;

        IF NOT EXISTS (
            SELECT 1 FROM pg_policies
            WHERE schemaname='public'
              AND tablename=tbl
              AND policyname='Authenticated users can update ' || tbl
        ) THEN
            EXECUTE format(
                'CREATE POLICY "Authenticated users can update %s"
                 ON public.%I
                 FOR UPDATE
                 TO authenticated
                 USING (true)
                 WITH CHECK (true);',
                tbl, tbl
            );
        END IF;

        IF NOT EXISTS (
            SELECT 1 FROM pg_policies
            WHERE schemaname='public'
              AND tablename=tbl
              AND policyname='Authenticated users can delete ' || tbl
        ) THEN
            EXECUTE format(
                'CREATE POLICY "Authenticated users can delete %s"
                 ON public.%I
                 FOR DELETE
                 TO authenticated
                 USING (true);',
                tbl, tbl
            );
        END IF;

    END LOOP;
END $$;