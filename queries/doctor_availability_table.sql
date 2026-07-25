-- doctor_availability table
CREATE TABLE doctor_availability (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    doctor_id UUID NOT NULL,

    weekday TEXT NOT NULL,

    start_time TIME NOT NULL,

    end_time TIME NOT NULL,

    is_available BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT fk_doctor
        FOREIGN KEY (doctor_id)
        REFERENCES doctors(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_weekday
        CHECK (
            weekday IN (
                'Monday',
                'Tuesday',
                'Wednesday',
                'Thursday',
                'Friday',
                'Saturday',
                'Sunday'
            )
        ),

    CONSTRAINT chk_time
        CHECK (start_time < end_time)

);

CREATE INDEX idx_doctor_availability_doctor
ON doctor_availability(doctor_id);

INSERT INTO doctor_availability
(
    doctor_id,
    weekday,
    start_time,
    end_time,
    is_available
)

SELECT
    d.id,
    s.weekday,
    s.start_time,
    s.end_time,
    TRUE

FROM doctors d

JOIN (

    /* Morning Shift */
    SELECT
        'Morning' AS shift,
        weekday,
        start_time,
        end_time
    FROM (
        VALUES
        ('Monday',    TIME '08:00', TIME '16:00'),
        ('Tuesday',   TIME '08:00', TIME '16:00'),
        ('Wednesday', TIME '08:00', TIME '16:00'),
        ('Thursday',  TIME '08:00', TIME '16:00'),
        ('Friday',    TIME '08:00', TIME '16:00'),
        ('Saturday',  TIME '09:00', TIME '13:00')
    ) x(weekday,start_time,end_time)

    UNION ALL

    /* General Shift */

    SELECT
        'General',
        weekday,
        start_time,
        end_time
    FROM (
        VALUES
        ('Monday',    TIME '09:00', TIME '17:00'),
        ('Tuesday',   TIME '09:00', TIME '17:00'),
        ('Wednesday', TIME '09:00', TIME '17:00'),
        ('Thursday',  TIME '09:00', TIME '17:00'),
        ('Friday',    TIME '09:00', TIME '17:00'),
        ('Saturday',  TIME '09:00', TIME '13:00'),
        ('Sunday',    TIME '10:00', TIME '14:00')
    ) x(weekday,start_time,end_time)

    UNION ALL

    /* Evening Shift */

    SELECT
        'Evening',
        weekday,
        start_time,
        end_time
    FROM (
        VALUES
        ('Monday',    TIME '12:00', TIME '20:00'),
        ('Tuesday',   TIME '12:00', TIME '20:00'),
        ('Wednesday', TIME '12:00', TIME '20:00'),
        ('Thursday',  TIME '12:00', TIME '20:00'),
        ('Friday',    TIME '12:00', TIME '20:00'),
        ('Saturday',  TIME '13:00', TIME '17:00')
    ) x(weekday,start_time,end_time)

) s

ON s.shift =

CASE

    WHEN d.specialization IN
    (
        'Cardiologist',
        'Neurologist',
        'Radiologist',
        'Ayurveda',
        'Homeopathy',
        'Siddha',
        'Naturopathy'
    )

    THEN 'Morning'

    WHEN d.specialization IN
    (
        'General Physician',
        'Dermatologist',
        'Pediatrician',
        'ENT',
        'Dentist',
        'Ophthalmologist',
        'Gynecologist',
        'Integrative Medicine'
    )

    THEN 'General'

    ELSE 'Evening'

END;

SELECT
    d.doctor_name,
    d.specialization,
    da.weekday,
    da.start_time,
    da.end_time
FROM doctor_availability da
JOIN doctors d
ON da.doctor_id = d.id
ORDER BY
    d.doctor_name,
    CASE da.weekday
        WHEN 'Monday' THEN 1
        WHEN 'Tuesday' THEN 2
        WHEN 'Wednesday' THEN 3
        WHEN 'Thursday' THEN 4
        WHEN 'Friday' THEN 5
        WHEN 'Saturday' THEN 6
        WHEN 'Sunday' THEN 7
    END;
