-- test queries for the medical interoperability database
-- useful and can be repurposed for making Analytics dashboards

-- Number of appointments per patient
SELECT
    p.patient_name,
    COUNT(a.id) AS total_appointments
FROM appointments a
JOIN patients p
    ON a.patient_id = p.id
GROUP BY
    p.patient_name
ORDER BY
    total_appointments DESC,
    p.patient_name;

-- Appointment count by doctor's specialization
SELECT
    d.specialization,
    COUNT(a.id) AS appointment_count
FROM appointments a
JOIN doctors d
    ON a.doctor_id = d.id
GROUP BY
    d.specialization
ORDER BY
    appointment_count DESC;

-- Complete Appointment Schedule
SELECT

    a.id AS appointment_id,

    p.patient_name,

    d.doctor_name,

    d.specialization,

    da.weekday,

    da.start_time,

    da.end_time,

    a.appointment_date,

    a.appointment_time,

    a.status

FROM appointments a

JOIN patients p
    ON a.patient_id = p.id

JOIN doctors d
    ON a.doctor_id = d.id

JOIN doctor_availability da
    ON da.doctor_id = d.id
   AND da.weekday = TO_CHAR(a.appointment_date, 'FMDay')

ORDER BY

    a.appointment_date,

    a.appointment_time;

-- Daily Appointment Statistics
SELECT

    appointment_date,

    COUNT(*) AS total_appointments

FROM appointments

GROUP BY appointment_date

ORDER BY appointment_date;

-- Appointment Status Distribution
SELECT

    status,

    COUNT(*) AS total

FROM appointments

GROUP BY status

ORDER BY total DESC;

-- Doctor Workload
SELECT

    d.doctor_name,

    d.specialization,

    COUNT(a.id) AS appointments

FROM doctors d

LEFT JOIN appointments a
    ON d.id = a.doctor_id

GROUP BY
    d.id,
    d.doctor_name,
    d.specialization

ORDER BY
    appointments DESC,
    d.doctor_name;

-- Upcoming Appointments
SELECT

    p.patient_name,

    d.doctor_name,

    a.appointment_date,

    a.appointment_time,

    a.status

FROM appointments a

JOIN patients p
    ON a.patient_id = p.id

JOIN doctors d
    ON a.doctor_id = d.id

WHERE a.appointment_date >= CURRENT_DATE

ORDER BY
    a.appointment_date,
    a.appointment_time;

-- Appointment Status per Doctor
SELECT
    d.doctor_name,
    a.status,
    COUNT(*) AS total
FROM appointments a
JOIN doctors d
    ON a.doctor_id = d.id
GROUP BY
    d.doctor_name,
    a.status
ORDER BY
    d.doctor_name,
    a.status;

-- Busiest Appointment Dates
SELECT
    appointment_date,
    COUNT(*) AS appointments
FROM appointments
GROUP BY appointment_date
ORDER BY appointments DESC
LIMIT 10;

-- Patients with Upcoming Visits
SELECT
    p.patient_name,
    d.doctor_name,
    d.specialization,
    a.appointment_date,
    a.appointment_time
FROM appointments a
JOIN patients p
    ON p.id = a.patient_id
JOIN doctors d
    ON d.id = a.doctor_id
WHERE
    a.appointment_date >= CURRENT_DATE
    AND a.status IN ('Pending', 'Confirmed')
ORDER BY
    a.appointment_date,
    a.appointment_time;


-- Doctors with Today's Appointments
SELECT
    d.doctor_name,
    COUNT(*) AS today_appointments
FROM appointments a
JOIN doctors d
    ON a.doctor_id = d.id
WHERE a.appointment_date = CURRENT_DATE
GROUP BY d.doctor_name
ORDER BY today_appointments DESC;

-- Patient Appointment History
SELECT
    p.patient_name,
    d.doctor_name,
    d.specialization,
    a.appointment_date,
    a.status
FROM appointments a
JOIN patients p
    ON p.id = a.patient_id
JOIN doctors d
    ON d.id = a.doctor_id
ORDER BY
    p.patient_name,
    a.appointment_date DESC;

-- Most Visited Doctors
SELECT
    d.doctor_name,
    d.specialization,
    COUNT(DISTINCT a.patient_id) AS unique_patients
FROM doctors d
LEFT JOIN appointments a
    ON d.id = a.doctor_id
GROUP BY
    d.id,
    d.doctor_name,
    d.specialization
ORDER BY unique_patients DESC;

-- Average Appointments per Day
SELECT
    ROUND(AVG(daily_count),2) AS average_daily_appointments
FROM (

    SELECT
        appointment_date,
        COUNT(*) AS daily_count

    FROM appointments

    GROUP BY appointment_date

) x;

-- Appointment Distribution by Weekday
SELECT
    TO_CHAR(appointment_date, 'Day') AS weekday,
    COUNT(*) AS appointments
FROM appointments
GROUP BY
    TO_CHAR(appointment_date, 'Day'),
    EXTRACT(DOW FROM appointment_date)
ORDER BY
    EXTRACT(DOW FROM appointment_date);

-- Doctor Utilization
SELECT
    d.doctor_name,
    d.specialization,
    COUNT(a.id) AS appointments,
    ROUND(
        COUNT(a.id) * 100.0 /
        SUM(COUNT(a.id)) OVER (),
        2
    ) AS percentage
FROM doctors d
LEFT JOIN appointments a
    ON d.id = a.doctor_id
GROUP BY
    d.id,
    d.doctor_name,
    d.specialization
ORDER BY appointments DESC;

-- Patient Visits by Status
SELECT
    p.patient_name,
    SUM(CASE WHEN status='Completed' THEN 1 ELSE 0 END) AS completed,
    SUM(CASE WHEN status='Confirmed' THEN 1 ELSE 0 END) AS confirmed,
    SUM(CASE WHEN status='Pending' THEN 1 ELSE 0 END) AS pending,
    SUM(CASE WHEN status='Cancelled' THEN 1 ELSE 0 END) AS cancelled
FROM appointments a
JOIN patients p
    ON p.id = a.patient_id
GROUP BY p.patient_name
ORDER BY completed DESC;

-- Available Doctors by Specialization
SELECT
    specialization,
    COUNT(*) AS doctors
FROM doctors
GROUP BY specialization
ORDER BY doctors DESC;

-- Doctor Working Hours
SELECT
    d.doctor_name,
    da.weekday,
    da.start_time,
    da.end_time
FROM doctor_availability da
JOIN doctors d
    ON d.id = da.doctor_id
ORDER BY
    d.doctor_name,
    da.weekday;

-- Appointment Timeline
SELECT
    appointment_date,
    status,
    COUNT(*) AS total
FROM appointments
GROUP BY
    appointment_date,
    status
ORDER BY appointment_date;

-- Patients Seen per Specialization
SELECT
    d.specialization,
    COUNT(DISTINCT a.patient_id) AS unique_patients
FROM appointments a
JOIN doctors d
    ON d.id = a.doctor_id
GROUP BY d.specialization
ORDER BY unique_patients DESC;

-- Dashboard KPI Query
SELECT

    (SELECT COUNT(*) FROM patients) AS total_patients,

    (SELECT COUNT(*) FROM doctors) AS total_doctors,

    (SELECT COUNT(*) FROM appointments) AS total_appointments,

    (SELECT COUNT(*) FROM appointments
        WHERE status='Completed') AS completed,

    (SELECT COUNT(*) FROM appointments
        WHERE status='Pending') AS pending,

    (SELECT COUNT(*) FROM appointments
        WHERE status='Confirmed') AS confirmed,

    (SELECT COUNT(*) FROM appointments
        WHERE status='Cancelled') AS cancelled;

-- Most Common Diagnoses
SELECT
    diagnosis,
    COUNT(*) AS total_cases
FROM medical_records
GROUP BY diagnosis
ORDER BY total_cases DESC;

-- diagnoses by doctor
SELECT

    d.doctor_name,

    COUNT(m.id) AS records_created

FROM medical_records m

JOIN doctors d
ON d.id = m.doctor_id

GROUP BY
    d.doctor_name

ORDER BY
    records_created DESC;

-- Diagnoses by Specialization
SELECT

    d.specialization,

    COUNT(*) AS diagnoses

FROM medical_records m

JOIN doctors d
ON d.id = m.doctor_id

GROUP BY
    d.specialization

ORDER BY
    diagnoses DESC;

-- daily medical records trend
SELECT

    DATE(created_at) AS record_date,

    COUNT(*) AS records

FROM medical_records

GROUP BY
    DATE(created_at)

ORDER BY
    record_date;

-- patient requiring follow-up
SELECT

    p.patient_name,

    d.doctor_name,

    diagnosis,

    follow_up_date

FROM medical_records m

JOIN patients p
ON p.id = m.patient_id

JOIN doctors d
ON d.id = m.doctor_id

WHERE follow_up_required = TRUE

ORDER BY
    follow_up_date;

-- follow-up statistics
SELECT

    follow_up_required,

    COUNT(*) AS total

FROM medical_records

GROUP BY
    follow_up_required;

-- patient medical history count
SELECT

    p.patient_name,

    COUNT(*) AS medical_records

FROM medical_records m

JOIN patients p
ON p.id = m.patient_id

GROUP BY
    p.patient_name

ORDER BY
    medical_records DESC;

-- doctor follow-up rate
SELECT

    d.doctor_name,

    COUNT(*) AS total_records,

    SUM(
        CASE
            WHEN follow_up_required
            THEN 1
            ELSE 0
        END
    ) AS followups

FROM medical_records m

JOIN doctors d
ON d.id = m.doctor_id

GROUP BY
    d.doctor_name

ORDER BY
    followups DESC;

-- diagnosis timeline
SELECT

    DATE(created_at) AS date,

    diagnosis,

    COUNT(*) AS total

FROM medical_records

GROUP BY

    DATE(created_at),

    diagnosis

ORDER BY

    date;

-- med records dashboard kpi
SELECT

COUNT(*) AS total_records,

COUNT(DISTINCT patient_id) AS patients,

COUNT(DISTINCT doctor_id) AS doctors,

SUM(
    CASE
        WHEN follow_up_required
        THEN 1
        ELSE 0
    END
) AS followups

FROM medical_records;

----------------------------------------------------
-- Current Stock per Medicine
SELECT
    m.name AS medicine,
    SUM(mi.quantity_in_stock) AS total_stock
FROM medicine_inventory mi
JOIN medicines m
ON mi.medicine_id = m.id
GROUP BY m.name
ORDER BY total_stock DESC;

-- Inventory Value
SELECT
    m.name,
    SUM(mi.quantity_in_stock * mi.unit_price) AS inventory_value
FROM medicine_inventory mi
JOIN medicines m
ON mi.medicine_id = m.id
GROUP BY m.name
ORDER BY inventory_value DESC;

-- medicines expring in next ~90 days
SELECT
    m.name,
    mi.batch_number,
    mi.expiry_date,
    mi.quantity_in_stock
FROM medicine_inventory mi
JOIN medicines m
ON mi.medicine_id = m.id
WHERE mi.expiry_date <= CURRENT_DATE + INTERVAL '90 days'
ORDER BY mi.expiry_date;

-- Expired Inventory
SELECT
    m.name,
    mi.batch_number,
    mi.expiry_date,
    mi.quantity_in_stock
FROM medicine_inventory mi
JOIN medicines m
ON mi.medicine_id = m.id
WHERE mi.expiry_date < CURRENT_DATE
ORDER BY mi.expiry_date;

-- number of batches per medicine
SELECT
    m.name,
    COUNT(*) AS total_batches
FROM medicine_inventory mi
JOIN medicines m
ON mi.medicine_id = m.id
GROUP BY m.name
ORDER BY total_batches DESC;

-- low stock medicines
SELECT
    m.name,
    SUM(mi.quantity_in_stock) AS stock
FROM medicine_inventory mi
JOIN medicines m
ON mi.medicine_id = m.id
GROUP BY m.name
HAVING SUM(mi.quantity_in_stock) < 100
ORDER BY stock;

-- average unit price
SELECT
    m.name,
    ROUND(AVG(mi.unit_price),2) AS average_price
FROM medicine_inventory mi
JOIN medicines m
ON mi.medicine_id = m.id
GROUP BY m.name
ORDER BY average_price DESC;

-- inventory kpi
SELECT

    COUNT(*) AS inventory_batches,

    COUNT(DISTINCT medicine_id) AS unique_medicines,

    SUM(quantity_in_stock) AS total_units,

    ROUND(
        SUM(quantity_in_stock * unit_price),
        2
    ) AS inventory_value

FROM medicine_inventory;

------------------------------------
-- Most Prescribed Medicines
SELECT
    m.name,
    COUNT(*) AS prescriptions
FROM prescriptions p
JOIN medicines m
ON p.medicine_id = m.id
GROUP BY m.name
ORDER BY prescriptions DESC;

-- Prescriptions per Diagnosis
SELECT
    mr.diagnosis,
    COUNT(*) AS total_prescriptions
FROM prescriptions p
JOIN medical_records mr
ON p.medical_record_uuid = mr.id
GROUP BY mr.diagnosis
ORDER BY total_prescriptions DESC;

-- Prescription Frequency Distribution
SELECT
    frequency,
    COUNT(*) AS total
FROM prescriptions
GROUP BY frequency
ORDER BY total DESC;

-- Medicines Prescribed by Doctor
SELECT
    d.doctor_name,
    m.name,
    COUNT(*) AS total
FROM prescriptions p
JOIN medical_records mr
ON p.medical_record_uuid = mr.id
JOIN doctors d
ON mr.doctor_id = d.id
JOIN medicines m
ON p.medicine_id = m.id
GROUP BY
    d.doctor_name,
    m.name
ORDER BY total DESC;

-- Prescription Timeline
SELECT
    prescribed_date,
    COUNT(*) AS prescriptions
FROM prescriptions
GROUP BY prescribed_date
ORDER BY prescribed_date;

-- Average Medicines per Medical Record
SELECT
ROUND(AVG(total),2) AS avg_medicines
FROM(

SELECT
medical_record_uuid,
COUNT(*) AS total
FROM prescriptions
GROUP BY medical_record_uuid

)x;

-- Dosage Usage
SELECT
    dosage,
    COUNT(*) AS total
FROM prescriptions
GROUP BY dosage
ORDER BY total DESC;

-- Prescription Dashboard KPI
SELECT

    COUNT(*) AS total_prescriptions,

    COUNT(DISTINCT medical_record_uuid) AS medical_records,

    COUNT(DISTINCT medicine_id) AS medicines_used,

    COUNT(DISTINCT prescribed_date) AS active_days

FROM prescriptions;


---------------------------------

-- Most Requested Lab Tests
SELECT
    report_name,
    COUNT(*) AS total
FROM lab_reports
GROUP BY report_name
ORDER BY total DESC;


-- Lab Reports by Diagnosis
SELECT
    mr.diagnosis,
    COUNT(*) AS reports
FROM lab_reports lr
JOIN medical_records mr
ON lr.medical_record_uuid = mr.id
GROUP BY mr.diagnosis
ORDER BY reports DESC;


-- Reports Generated by Doctor
SELECT
    d.doctor_name,
    COUNT(*) AS reports
FROM lab_reports lr
JOIN medical_records mr
ON lr.medical_record_uuid = mr.id
JOIN doctors d
ON mr.doctor_id = d.id
GROUP BY d.doctor_name
ORDER BY reports DESC;


-- Daily Lab Report Trend
SELECT
    DATE(created_at) AS report_date,
    COUNT(*) AS reports
FROM lab_reports
GROUP BY DATE(created_at)
ORDER BY report_date;


-- Patients Receiving Maximum Lab Reports
SELECT
    p.patient_name,
    COUNT(*) AS reports
FROM lab_reports lr
JOIN medical_records mr
ON lr.medical_record_uuid = mr.id
JOIN patients p
ON mr.patient_id = p.id
GROUP BY p.patient_name
ORDER BY reports DESC;


-- Lab Reports per Specialization
SELECT
    d.specialization,
    COUNT(*) AS reports
FROM lab_reports lr
JOIN medical_records mr
ON lr.medical_record_uuid = mr.id
JOIN doctors d
ON mr.doctor_id = d.id
GROUP BY d.specialization
ORDER BY reports DESC;


-- Diagnoses Requiring Labs
SELECT
    mr.diagnosis,
    COUNT(*) AS reports_generated
FROM lab_reports lr
JOIN medical_records mr
ON lr.medical_record_uuid = mr.id
GROUP BY mr.diagnosis
ORDER BY reports_generated DESC;


-- Lab Report Dashboard KPI
SELECT

    COUNT(*) AS total_reports,

    COUNT(DISTINCT report_name) AS report_types,

    COUNT(DISTINCT medical_record_uuid) AS medical_records,

    COUNT(DISTINCT DATE(created_at)) AS reporting_days

FROM lab_reports;