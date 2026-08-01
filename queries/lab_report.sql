-- ==========================================================
-- LAB REPORTS
-- ==========================================================

CREATE TABLE public.lab_reports (

    report_uuid UUID PRIMARY KEY
        DEFAULT gen_random_uuid(),

    medical_record_uuid UUID NOT NULL,

    report_name VARCHAR(100) NOT NULL,

    report_url TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT NOW(),

    CONSTRAINT fk_lab_report_medical_record
        FOREIGN KEY (medical_record_uuid)
        REFERENCES public.medical_records(id)
        ON DELETE CASCADE

);

-- ----------------------------------------------------------
-- Helpful Indexes
-- ----------------------------------------------------------

CREATE INDEX idx_lab_reports_medical_record
ON public.lab_reports(medical_record_uuid);

CREATE INDEX idx_lab_reports_report_name
ON public.lab_reports(report_name);