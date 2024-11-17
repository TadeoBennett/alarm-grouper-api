SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE `groups`;

INSERT INTO `groups` VALUES
(NULL, 1, 'Work Alarms', 'A set of alarms for every weekday at work.', NOW()),
(NULL, 1, 'Chore Days', 'Alarms for different chores to do on different days', NOW());
