-- Триггер для автоматического добавления даты регистрации при создании нового пользователя
CREATE TRIGGER IF NOT EXISTS trg_user_registration_date
AFTER INSERT ON users
BEGIN
    UPDATE users 
    SET registration_date = CURRENT_TIMESTAMP 
    WHERE user_id = NEW.user_id;
END;

-- Триггер для автоматического добавления даты при назначении администратора
CREATE TRIGGER IF NOT EXISTS trg_admin_added_date
AFTER INSERT ON admins
BEGIN
    UPDATE admins 
    SET added_date = CURRENT_TIMESTAMP 
    WHERE user_id = NEW.user_id;
END;

-- Триггер для проверки существования пользователя перед добавлением администратора
CREATE TRIGGER IF NOT EXISTS trg_check_user_exists
BEFORE INSERT ON admins
BEGIN
    SELECT CASE
        WHEN NOT EXISTS (SELECT 1 FROM users WHERE user_id = NEW.user_id)
        THEN RAISE(ABORT, 'User does not exist')
    END;
END;

-- Триггер для логирования изменений языка пользователя
CREATE TRIGGER IF NOT EXISTS trg_log_language_change
AFTER UPDATE OF lang ON users
BEGIN
    INSERT INTO language_change_log (user_id, old_lang, new_lang, change_date)
    VALUES (NEW.user_id, OLD.lang, NEW.lang, CURRENT_TIMESTAMP);
END; 