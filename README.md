# 🏥 Medical Interpolarbility

> A centralized healthcare platform built using **Streamlit** and **Supabase** to securely consolidate a patient's lifelong medical history while providing hospitals and administrators with powerful analytics and operational insights.
---
## About the Project

Medical records are often scattered across different hospitals, clinics and diagnostic centers. Patients may unintentionally lose prescriptions, forget previous diagnoses, or struggle to provide their complete medical history during emergencies.

**Medical Interpolarbility** aims to solve this problem by acting as a centralized healthcare record management platform.

Instead of every hospital maintaining isolated records, this platform provides a single source of truth where patient information, appointments, doctors, prescriptions, medical records and laboratory reports can all be connected together.

The project also serves hospitals and healthcare administrators by providing analytics that help understand operational trends such as:

- Which specialization receives the most appointments
- Which doctor has the highest workload
- Appointment completion rates
- Patient demographics
- Weekly appointment distribution
- Hospital-wide performance metrics

The objective is to improve both **patient healthcare continuity** and **hospital decision making**.

---

# Why this Project?

One of the biggest problems in healthcare today is fragmented patient information.

Imagine a patient visiting:

- Hospital A
- Hospital B
- Hospital C

Each hospital stores its own records independently.

Months later, the patient may no longer remember:

- Previous diagnosis
- Allergies
- Prescribed medicines
- Previous laboratory reports
- Earlier treatments
- Doctor recommendations

This often results in:

- Duplicate medical tests
- Incorrect prescriptions
- Missing allergies
- Longer diagnosis time
- Increased healthcare costs

Medical Interpolarbility aims to become a centralized healthcare ecosystem where patient records remain available throughout their lifetime instead of being tied to a single hospital.

---

# 🎯 Project Objectives

The project focuses on four primary goals.

### For Patients

- Maintain a lifelong medical history
- Never lose prescriptions again
- Keep allergies and medical conditions available
- Easily share records with doctors
- Maintain one unified health profile

---

### For Doctors

- View previous patient history instantly
- Access previous diagnoses
- Review prescriptions
- Upload medical records
- Maintain continuity of care

---

### For Hospitals

- Analyze appointment trends
- Measure doctor workload
- Understand patient demographics
- Improve resource allocation
- Make data-driven operational decisions

---

### For Administrators

- Complete dashboard analytics
- Patient management
- Doctor management
- Appointment monitoring
- Hospital performance insights

---

# Current Features

## 📊 Analytics Dashboard

The current implementation focuses on an interactive analytics dashboard built using Streamlit.

### Dashboard KPIs

- Total Patients
- Total Doctors
- Total Appointments
- Completed Appointments
- Pending Appointments
- Confirmed Appointments
- Cancelled Appointments
- Appointment Completion Rate

---

### Patient Analytics

- Patient Age Distribution
- Blood Group Distribution
- Average Height
- Average Weight

---

### Appointment Analytics

- Appointment Status Distribution
- Daily Appointment Trends
- Weekday Appointment Analysis
- Appointment Status by Specialization

---

### Doctor Analytics

- Doctor Workload
- Appointments by Specialization
- Doctors per Specialization
- Most Active Doctors

---

### Patient Analytics

- Most Frequent Patients

---

### Administrative Features

- Database Explorer
- Doctor Availability Viewer
- Quick Insight Cards
- Summary Statistics

---

# Planned Features

The project is currently under active development.

Upcoming modules include:

- Patient Portal
- Doctor Portal
- Medical Records Module
- Prescription Management
- Laboratory Report Storage
- Appointment Scheduling
- Authentication & Authorization
- Role Based Access Control
- Supabase Row Level Security
- Report Uploads
- Doctor Availability Scheduling
- Advanced Admin Dashboard
- Search & Filtering
- Patient Timeline View

---

# 🛠 Tech Stack

| Category | Technology |
|-----------|------------|
| Language | Python |
| Frontend | Streamlit |
| Backend | Supabase |
| Database | PostgreSQL (Supabase) |
| Data Analysis | Pandas |
| Visualization | Plotly |
| Authentication *(Planned)* | Supabase Auth |
| Storage *(Planned)* | Supabase Storage |

---

# 📂 Project Structure

<pre>
medical_interpolarbility/
│
├── assets/
│   ├── medical_interpolarbility_full_image.png
│   └── medical_interpolarbility_tranparent_bg_1.png
│   └── medical_interpolator_repo_banner.png
│
├── pages/
│   └── 1_Analytics.py
│
├── queries/
│   ├── patient_table.sql
│   ├── doctor_table.sql
│   ├── doctor_availability_table.sql
│   ├── appointment_table.sql
│   ├── db_master.sql
│   └── tests/
│       └── test_queries.sql
│
├── scripts/
│   └── seed_db.py
│
├── services/
│   ├── analytics_service.py
│   └── supabase_service.py
│
├── app.py
├── db_schema.txt
├── schema_design.txt
├── .gitignore
└── README.md
</pre>

---

# 📁 Folder Overview

| Folder | Purpose |
|---------|----------|
| **assets/** | Project logo and graphical assets |
| **pages/** | Streamlit multi-page application pages |
| **queries/** | SQL scripts for creating database tables |
| **queries/tests/** | SQL queries used for testing |
| **scripts/** | Utility scripts such as database seeding |
| **services/** | Business logic and Supabase interaction |
| **app.py** | Main Streamlit application entry point |
| **db_schema.txt** | Database schema reference |
| **schema_design.txt** | Complete database design documentation |

---

# 📂 API & File Reference

## 1. `app.py`
| Component / Function | Description |
|---|---|
| `st.set_page_config(...)` | Configures the Streamlit page layout, title, icon, and sidebar state. |
| `st.title(...)` / `st.markdown(...)` | Renders the main dashboard welcome UI, module list, and phase information. |

---

## 2. `pages/`

### `1_Analytics.py`
| Function / Component | Description |
|---|---|
| `render_graph(title, df, empty_msg, chart_fn, insight_fn)` | Reusable helper to render a Plotly chart with a title, empty state message, and dynamic insight text. |
| `st.metric(...)` | Renders KPI cards for patients, doctors, appointments, and completion rates. |
| `st.tabs(...)` | Creates the Database Explorer tabs for viewing raw table data. |

---

## 3. `services/`

### `analytics_service.py`
| Function / Method | Description |
|---|---|
| `__init__()` | Initializes the Supabase client connection via `SupabaseService`. |
| `get_patients()` | Fetches all records from the `patients` table. |
| `get_doctors()` | Fetches all records from the `doctors` table. |
| `get_appointments()` | Fetches all records from the `appointments` table. |
| `get_doctor_availability()` | Fetches all records from the `doctor_availability` table. |
| `get_summary_text()` | Generates a text summary of overall system KPIs and statuses. |
| `get_highlight_text()` | Generates highlight text for the top specialization workload. |
| `get_dashboard_kpis()` | Calculates and returns core dashboard metrics (counts, rates). |
| `get_age_distribution()` | Calculates patient age distribution based on DOB. |
| `get_blood_group_distribution()` | Counts patients per blood group. |
| `get_average_height()` | Calculates the mean height of all patients. |
| `get_average_weight()` | Calculates the mean weight of all patients. |
| `get_status_distribution()` | Counts appointments by status (Pending, Completed, etc.). |
| `get_daily_appointments()` | Groups appointments by date for trend analysis. |
| `get_weekday_distribution()` | Groups appointments by day of the week. |
| `get_specialization_distribution()` | Counts appointments grouped by doctor specialization. |
| `get_doctor_workload()` | Calculates total appointments per doctor. |
| `get_status_by_specialization()` | Cross-references appointment status with specialization. |
| `get_top_doctors(limit)` | Returns the top N doctors by appointment volume. |
| `get_top_patients(limit)` | Returns the top N patients by appointment volume. |
| `get_insights()` | Generates a list of quick textual insights for the dashboard. |
| `get_specialization_workload()` | Calculates appointment count grouped by specialization. |
| `get_doctors_per_specialization()` | Counts the number of doctors in each specialization. |

### `supabase_service.py`
| Function / Method | Description |
|---|---|
| `get_client()` | Singleton class method that initializes and returns the Supabase client using `.streamlit/secret.toml`. |

---

## 4. `scripts/`

### `seed_db.py`
| Function | Description |
|---|---|
| `weighted_choice(doctors)` | Selects a random doctor based on predefined specialization weights. |
| `random_status(appointment_date)` | Determines appointment status (Completed, Pending, etc.) based on the date. |
| `random_datetime(days)` | Generates a random date within a ±days range from today. |
| `print_header(title)` | Prints a formatted console header for script execution logs. |
| `random_time_between(start_time, end_time)` | Generates a random time slot between a start and end time. |
| `next_matching_weekday(target_weekday)` | Finds the next upcoming date that matches a specific weekday. |

---

## 5. `queries/`

### `patient_table.sql`
| Table / View / Operation | Description |
|---|---|
| `patients` (Table) | Alters schema, adds constraints (DOB, height, weight, allergies), and populates sample data. |
| `patient_details` (View) | Creates a view to display patient details with a dynamically calculated `age` column. |

### `doctor_table.sql`
| Table / View / Operation | Description |
|---|---|
| `doctors` (Table) | Creates the doctors table and inserts 20 sample doctor records with various specializations. |

### `doctor_availability_table.sql`
| Table / View / Operation | Description |
|---|---|
| `doctor_availability` (Table) | Creates availability schedules, enforces weekday/time constraints, and populates shifts based on specialization. |

### `appointment_table.sql`
| Table / View / Operation | Description |
|---|---|
| `appointments` (Table) | Creates the appointments table with foreign keys to patients and doctors, and adds performance indexes. |

### `db_master.sql`
| Table / View / Operation | Description |
|---|---|
| Master Schema | Consolidates the creation and population of `patients`, `doctors`, `doctor_availability`, `appointments`, and the `patient_details` view. |

### `test_queries.sql`
| Query Purpose | Description |
|---|---|
| Dashboard KPI Query | Aggregates total counts for patients, doctors, and appointment statuses. |
| Doctor Workload / Utilization | Calculates total appointments and percentage utilization per doctor. |
| Appointment Analytics | Groups appointments by date, weekday, status, and specialization. |
| Patient History / Activity | Retrieves appointment history, frequent patients, and upcoming visits. |

---
