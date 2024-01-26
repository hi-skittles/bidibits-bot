-- CREATE TABLE IF NOT EXISTS `warns` (
--   `id` int(11) NOT NULL,
--   `user_id` varchar(20) NOT NULL,
--   `server_id` varchar(20) NOT NULL,
--   `moderator_id` varchar(20) NOT NULL,
--   `reason` varchar(255) NOT NULL,
--   `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
-- );
CREATE TABLE IF NOT EXISTS "blacklisted_users" (
    "user_id" INTEGER NOT NULL UNIQUE,
    "username" TEXT NOT NULL,
    "reason_optional" TEXT(255),
    "added_at_timestamp" timestamp DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("user_id")
);

CREATE TABLE IF NOT EXISTS "debug_dev_settings" (
	"logging_server_id"	INTEGER NOT NULL,
	"primary_log_channel_id"	INTEGER NOT NULL,
	"debug_log_channel_id"	INTEGER NOT NULL,
	"critical_log_channel_id"	INTEGER NOT NULL
);