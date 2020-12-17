CREATE DATABASE IF NOT EXISTS `onlinemedicalconsultation` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `onlinemedicalconsultation`;
show databases;

CREATE TABLE IF NOT EXISTS `accounts`(
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`username`VARCHAR(50) NOT NULL,
	`email` VARCHAR(255)NOT NULL,
	`password` VARCHAR(100)NOT NULL,
	PRIMARY KEY (`id`) 
    ) ENGINE = InnoDB AUTO_INCREMENT =2 DEFAULT CHARSET =utf8;

CREATE TABLE IF NOT EXISTS `bookappointment` (
    appoint_id int NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL ,
    fullname VARCHAR(50) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    appoint_date DATE NOT NULL,
    contact_no VARCHAR(20) NOT NULL,
    symptoms VARCHAR(255) NOT NULL,
    report_file LONGBLOB , 
	PRIMARY KEY (`appoint_id`),
    FOREIGN KEY(`user_id`) REFERENCES accounts(id)
)ENGINE = InnoDB AUTO_INCREMENT =2 DEFAULT CHARSET =utf8;
 
CREATE TABLE IF NOT EXISTS `contact_info` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `fullname`VARCHAR(50) NOT NULL,
    `email` VARCHAR(255)NOT NULL,
    `msg` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`)
    ) ENGINE = InnoDB AUTO_INCREMENT =2 DEFAULT CHARSET =utf8;

