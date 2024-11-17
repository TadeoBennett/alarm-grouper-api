SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE users;

INSERT INTO users VALUES
(NULL, 'TBennett', 'tadeos.bennett@gmail.com', 'password', NOW()),
(NULL, 'JDoe', 'johndoe@gmail.com', 'password', NOW());