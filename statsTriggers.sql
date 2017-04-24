CREATE TRIGGER client_stats AFTER INSERT ON connection
BEGIN
  UPDATE client SET
    nCon = (SELECT COUNT(*) FROM connection WHERE client = NEW.client),
    totalTime = (SELECT SUM(duration) FROM connection WHERE client = NEW.client),
    maxTime = (SELECT MAX(duration) FROM connection WHERE client = NEW.client)
    WHERE id = NEW.client;
END;
