SELECT
    t.id,
    t.title,
    a.full_name AS assigned_to,
    t.status,
    t.progress,
    t.start_date,
    t.end_date
FROM tasks t
JOIN admins a
ON t.assigned_to = a.id;