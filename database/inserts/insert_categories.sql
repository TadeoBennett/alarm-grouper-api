SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE categories;

INSERT INTO categories VALUES
(NULL, 1, 1, 'Monday Schedule Alarms', 'Alarms for Mondays at work', NOW()),
(NULL, 1, 1, 'Tuesday Schedule Alarms', '', NOW()),
(NULL, 2, 2, 'Morning Chores', 'This needs to get done by 11am', NOW()),
(NULL, 2, 2, 'Afternoon Chores', 'This needs to get done by 2pm', NOW());
