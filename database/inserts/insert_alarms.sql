SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE `alarms`;

INSERT INTO `alarms` VALUES
(NULL, 1, 1, 'Meeting a 8am with Agnes', '', '08:00', '2024-10-17', 0, 1, 0, NOW()),
(NULL, 1, 1, 'Call the Boss', '', '08:00', '2024-08-17', 0, 1, 0, NOW()),

(NULL, 2, 2, 'Wipe the windows', "", '07:00', '2024-10-17', 1, 2, 0, NOW()),
(NULL, 2, 2, 'Mop the floors', "", '07:00', '2024-10-17', 1, 2, 0, NOW());
