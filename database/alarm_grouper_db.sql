-- MySQL Script generated by MySQL Workbench
-- Wed Oct 16 23:54:34 2024
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema alarm_grouper
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `alarm_grouper` ;

-- -----------------------------------------------------
-- Schema alarm_grouper
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `alarm_grouper` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `alarm_grouper` ;

-- -----------------------------------------------------
-- Table `alarm_grouper`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `alarm_grouper`.`users` ;

CREATE TABLE IF NOT EXISTS `alarm_grouper`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(30) NOT NULL,
  `email` VARCHAR(70) NOT NULL,
  `password` VARCHAR(256) NOT NULL,
  `created_at` TIMESTAMP NULL DEFAULT now(),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username` (`username` ASC) VISIBLE,
  UNIQUE INDEX `email` (`email` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `alarm_grouper`.`groups`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `alarm_grouper`.`groups` ;

CREATE TABLE IF NOT EXISTS `alarm_grouper`.`groups` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `group_creator_id` INT NOT NULL,
  `name` VARCHAR(30) NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `created_at` TIMESTAMP NULL DEFAULT now(),
  PRIMARY KEY (`id`),
  INDEX `group_creator_id` (`group_creator_id` ASC) VISIBLE,
  CONSTRAINT `groups_ibfk_1`
    FOREIGN KEY (`group_creator_id`)
    REFERENCES `alarm_grouper`.`users` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `alarm_grouper`.`categories`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `alarm_grouper`.`categories` ;

CREATE TABLE IF NOT EXISTS `alarm_grouper`.`categories` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `category_creator_id` INT NOT NULL,
  `group_id` INT NULL DEFAULT NULL,
  `name` VARCHAR(30) NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `created_at` TIMESTAMP NULL DEFAULT now(),
  PRIMARY KEY (`id`),
  INDEX `category_creator_id` (`category_creator_id` ASC) VISIBLE,
  INDEX `group_id` (`group_id` ASC) VISIBLE,
  CONSTRAINT `categories_ibfk_1`
    FOREIGN KEY (`category_creator_id`)
    REFERENCES `alarm_grouper`.`users` (`id`),
  CONSTRAINT `categories_ibfk_2`
    FOREIGN KEY (`group_id`)
    REFERENCES `alarm_grouper`.`groups` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `alarm_grouper`.`sounds`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `alarm_grouper`.`sounds` ;

CREATE TABLE IF NOT EXISTS `alarm_grouper`.`sounds` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `sound_creator_id` INT NOT NULL DEFAULT '0',
  `name` VARCHAR(20) NOT NULL,
  `file` VARCHAR(50) NOT NULL,
  `description` VARCHAR(50) NULL,
  `created_at` TIMESTAMP NULL DEFAULT now(),
  PRIMARY KEY (`id`),
  INDEX `sound_creator_id` (`sound_creator_id` ASC) VISIBLE,
  CONSTRAINT `sound_creator_id`
    FOREIGN KEY (`sound_creator_id`)
    REFERENCES `alarm_grouper`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `alarm_grouper`.`alarms`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `alarm_grouper`.`alarms` ;

CREATE TABLE IF NOT EXISTS `alarm_grouper`.`alarms` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `alarm_creator_id` INT NULL DEFAULT NULL,
  `category_id` INT NULL DEFAULT NULL,
  `name` VARCHAR(30) NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `ringTime` TIME NULL DEFAULT NULL,
  `ringDate` DATE NULL DEFAULT NULL,
  `repeat` TINYINT NULL DEFAULT '0',
  `sound_id` INT NULL DEFAULT NULL,
  `active` TINYINT NULL DEFAULT '0',
  `created_at` TIMESTAMP NULL DEFAULT now(),
  PRIMARY KEY (`id`),
  INDEX `alarm_creator_id` (`alarm_creator_id` ASC) VISIBLE,
  INDEX `category_id` (`category_id` ASC) VISIBLE,
  INDEX `sound_id` (`sound_id` ASC) VISIBLE,
  CONSTRAINT `alarms_ibfk_1`
    FOREIGN KEY (`alarm_creator_id`)
    REFERENCES `alarm_grouper`.`users` (`id`),
  CONSTRAINT `alarms_ibfk_2`
    FOREIGN KEY (`category_id`)
    REFERENCES `alarm_grouper`.`categories` (`id`),
  CONSTRAINT `alarms_ibfk_3`
    FOREIGN KEY (`sound_id`)
    REFERENCES `alarm_grouper`.`sounds` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
