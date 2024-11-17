SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE sounds;

INSERT INTO sounds VALUES
(NULL, 1, 'phonk', '/default/phonk.mp3', '', NOW()),
(NULL, 1, 'rock', '/default/rock.mp3', '', NOW()),
(NULL, 2, 'daylight', '/default/daylight.mp3', '', NOW()),
(NULL, 2, 'sunset', '/default/sunset.mp3', '', NOW());
