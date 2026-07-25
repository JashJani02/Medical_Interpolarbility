-- doctor table
CREATE TABLE doctors (

    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    doctor_name TEXT NOT NULL,

    doctor_phone TEXT NOT NULL UNIQUE,

    hospital_address TEXT NOT NULL,

    specialization TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()

);

-- populate the doctors table with sample data
INSERT INTO doctors (
    doctor_name,
    doctor_phone,
    hospital_address,
    specialization
)
VALUES
(
    'Dr. Rajesh Shah',
    '+919876543210',
    'Apollo Hospital, Ahmedabad, Gujarat',
    'Cardiologist'
),
(
    'Dr. Priya Patel',
    '+919876543211',
    'Sterling Hospital, Ahmedabad, Gujarat',
    'Dermatologist'
),
(
    'Dr. Amit Kumar',
    '+919876543212',
    'Civil Hospital, Ahmedabad, Gujarat',
    'Neurologist'
),
(
    'Dr. Neha Sharma',
    '+919876543213',
    'KD Hospital, Ahmedabad, Gujarat',
    'Pediatrician'
),
(
    'Dr. Vivek Mehta',
    '+919876543214',
    'Zydus Hospital, Ahmedabad, Gujarat',
    'Orthopedic'
),
(
    'Dr. Rina Desai',
    '+919876543215',
    'Shalby Hospital, Ahmedabad, Gujarat',
    'General Physician'
),
(
    'Dr. Arjun Joshi',
    '+919876543216',
    'HCG Cancer Centre, Ahmedabad, Gujarat',
    'Oncologist'
),
(
    'Dr. Kavita Rao',
    '+919876543217',
    'CIMS Hospital, Ahmedabad, Gujarat',
    'Psychiatrist'
),
(
    'Dr. Harsh Trivedi',
    '+919876543218',
    'Narayana Multispeciality Hospital, Ahmedabad, Gujarat',
    'ENT'
),
(
    'Dr. Sneha Iyer',
    '+919876543219',
    'Wockhardt Hospital, Rajkot, Gujarat',
    'Gynecologist'
),
(
    'Dr. Nikhil Soni',
    '+919876543220',
    'Sunshine Global Hospital, Vadodara, Gujarat',
    'Radiologist'
),
(
    'Dr. Meera Nair',
    '+919876543221',
    'SAL Hospital, Ahmedabad, Gujarat',
    'Ophthalmologist'
),
(
    'Dr. Rohit Kapoor',
    '+919876543222',
    'UN Mehta Institute of Cardiology, Ahmedabad, Gujarat',
    'Cardiologist'
),
(
    'Dr. Asha Menon',
    '+919876543223',
    'Care Institute of Medical Sciences (CIMS), Ahmedabad, Gujarat',
    'Dermatologist'
),
(
    'Dr. Karan Malhotra',
    '+919876543224',
    'Civil Hospital, Surat, Gujarat',
    'Dentist'
),
(    'Dr. Anjali Joshi',
    '+919876543235',
    'Ayush Wellness Centre, Ahmedabad, Gujarat',
    'Ayurveda'
),
(
    'Dr. Rakesh Verma',
    '+919876543236',
    'National Homeopathy Clinic, Vadodara, Gujarat',
    'Homeopathy'
),
(
    'Dr. Mehul Bhatt',
    '+919876543237',
    'Siddha Medical Centre, Chennai, Tamil Nadu',
    'Siddha'
),
(
    'Dr. Pooja Iyer',
    '+919876543238',
    'Naturopathy & Yoga Institute, Bengaluru, Karnataka',
    'Naturopathy'
),
(
    'Dr. Sanjay Kulkarni',
    '+919876543239',
    'Integrated Healthcare Centre, Pune, Maharashtra',
    'Integrative Medicine'
);