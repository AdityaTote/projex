DROP TRIGGER IF EXISTS tokens_updated_at ON tokens;

DROP FUNCTION IF EXISTS update_updated_at_column();

DROP TABLE IF EXISTS chats;

DROP TABLE IF EXISTS sessions;

DROP TABLE IF EXISTS tokens;

DROP TABLE IF EXISTS users;
