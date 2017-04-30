-- by ToFran
-- https://github.com/ToFran/TS3LogAnalyzer

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS user ( --used for merging clients (has multiple clients)
	user_id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	mainNickname TEXT,
	nCon	INTEGER NOT NULL DEFAULT 0,
	totalTime	INTEGER NOT NULL DEFAULT 0,
	maxTime	INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS client ( --represents a TS3 client
	client_id	INTEGER NOT NULL PRIMARY KEY,
	mainNickname TEXT,
	nCon	INTEGER NOT NULL DEFAULT 0,
	totalTime	INTEGER NOT NULL DEFAULT 0,
	maxTime	INTEGER NOT NULL DEFAULT 0,
	user_id INTEGER,
	FOREIGN KEY(user_id) REFERENCES user(user_id)
);

CREATE TABLE IF NOT EXISTS connection (
	connection_id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	connected	INTEGER NOT NULL,
	disconnected	INTEGER NOT NULL,
	reason	INTEGER NOT NULL,
	ip	TEXT NOT NULL,
	server	INTEGER NOT NULL DEFAULT 0,
	duration INTEGER NOT NULL DEFAULT 0,
	client_id	INTEGER NOT NULL,
	log_id INTEGER NOT NULL,
	FOREIGN KEY(client_id) REFERENCES client(client_id),
	FOREIGN KEY(log_id) REFERENCES log(log_id)
);

CREATE TABLE IF NOT EXISTS nickname (
	client_id	INTEGER NOT NULL,
	nickname	TEXT NOT NULL,
	used	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY(client_id, nickname),
	FOREIGN KEY(client_id) REFERENCES client(client_id)
);

CREATE TABLE IF NOT EXISTS log (
	log_id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	filename	TEXT NOT NULL UNIQUE,
	lastanalysis TEXT NOT NULL,
	lines	INTEGER NOT NULL DEFAULT 0,
	size INTEGER NOT NULL DEFAULT 0
);

CREATE TRIGGER TR_client_update AFTER UPDATE ON client
	WHEN NEW.user_id <> NULL AND NEW.user_id <> OLD.user_id
BEGIN
	--makes all brother clients point to the same father
	UPDATE client SET
		user_id = NEW.user_id
		WHERE user_id = OLD.user_id;

	--delete lossen users
	DELETE FROM user
		WHERE user_id = OLD.user_id;

	--update parent stats
  UPDATE user SET
    nCon = (SELECT SUM(nCon) FROM client WHERE user_id = NEW.user_id),
    totalTime = (SELECT SUM(totalTime) FROM client WHERE user_id = NEW.user_id),
    maxTime = (SELECT MAX(maxTime) FROM client WHERE user_id = NEW.user_id)
    WHERE user_id = NEW.user_id;
END;
