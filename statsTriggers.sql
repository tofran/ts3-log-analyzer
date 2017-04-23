CREATE TRIGGER client_stats AFTER INSERT ON connection
BEGIN
  UPDATE client SET
    nCon = (SELECT COUNT(*) FROM connection WHERE client = NEW.client),
    totalTime = (SELECT SUM(duration) FROM connection WHERE client = NEW.client),
    maxTime = (SELECT MAX(duration) FROM connection WHERE client = NEW.client);
END;


CREATE TRIGGER user_stats AFTER UPDATE ON client WHEN NEW.user <> NULL
BEGIN
  UPDATE user SET
    nCon = (SELECT SUM(nCon) FROM client WHERE user = NEW.user),
    totalTime = (SELECT SUM(duration) FROM client WHERE user = NEW.user),
    maxTime = (SELECT MAX(duration) FROM client WHERE user = NEW.user);
END;
