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