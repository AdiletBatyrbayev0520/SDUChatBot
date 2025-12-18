-- Удаление индексов
DROP INDEX IF EXISTS idx_users_registration_date;
DROP INDEX IF EXISTS idx_admins_added_date;

-- Удаление таблиц
DROP TABLE IF EXISTS admins;
DROP TABLE IF EXISTS users; 