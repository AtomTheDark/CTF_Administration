CREATE TABLE `teams`(
    `team_id_pk` INT NOT NULL,
    `team_name` VARCHAR(255) NULL,
    PRIMARY KEY(`team_id_pk`)
);
ALTER TABLE
    `teams` ADD UNIQUE `teams_team_name_unique`(`team_name`);
CREATE TABLE `admins`(
    `admin_id_pk` INT NOT NULL,
    `username` VARCHAR(255) NULL,
    `email` VARCHAR(255) NULL,
    `admin_password_hash` VARCHAR(255) NOT NULL,
    `created_at` DATETIME NULL,
    PRIMARY KEY(`admin_id_pk`)
);
ALTER TABLE
    `admins` ADD UNIQUE `admins_username_unique`(`username`);
ALTER TABLE
    `admins` ADD UNIQUE `admins_email_unique`(`email`);
CREATE TABLE `challenges`(
    `challenge_id_pk` INT NOT NULL,
    `competition_id_fk` INT NOT NULL,
    `title` VARCHAR(255) NOT NULL,
    `description` VARCHAR(255) NULL,
    `cat_id_fk` INT NULL,
    `difficulty` VARCHAR(255) NOT NULL,
    `points` INT NULL,
    `encrypted_flag` VARCHAR(255) NULL,
    `admin_id_fk` INT NULL,
    `created_at` DATETIME NOT NULL,
    PRIMARY KEY(`challenge_id_pk`)
);
ALTER TABLE
    `challenges` ADD UNIQUE `challenges_encrypted_flag_unique`(`encrypted_flag`);
CREATE TABLE `categories`(
    `cat_id_pk` INT NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    PRIMARY KEY(`cat_id_pk`)
);
CREATE TABLE `submissions`(
    `submission_id` INT NOT NULL,
    `team_id_fk` INT NOT NULL,
    `challenge_id_fk` INT NOT NULL,
    `submitted_flag` VARCHAR(255) NOT NULL,
    `is_correct` BOOLEAN NOT NULL,
    `submitted_at` DATETIME NOT NULL,
    PRIMARY KEY(`submission_id`)
);
CREATE TABLE `players`(
    `player_id_pk` INT NOT NULL,
    `player_name` VARCHAR(255) NOT NULL,
    `player_username` VARCHAR(255) NOT NULL,
    `player_passwd_hash` VARCHAR(255) NOT NULL,
    PRIMARY KEY(`player_id_pk`)
);
CREATE TABLE `scores`(
    `team_id_pfk` INT NOT NULL,
    `total_points` INT NOT NULL,
    `challenges_solved` INT NOT NULL,
    PRIMARY KEY(`team_id_pfk`)
);
CREATE TABLE `hints`(
    `hint_id` INT NOT NULL,
    `challenge_id_fk` INT NOT NULL,
    `hint_text` TEXT NOT NULL,
    `cost` INT NOT NULL,
    PRIMARY KEY(`hint_id`)
);
CREATE TABLE `team_members`(
    `team_id_fk` INT NOT NULL,
    `player_id_fk` INT NOT NULL,
    PRIMARY KEY(`team_id_fk`,`player_id_fk`)
);
CREATE TABLE `competitions`(
    `competition_id_pk` INT NOT NULL,
    `competition_name` VARCHAR(255) NOT NULL,
    `description` VARCHAR(255) NOT NULL,
    `admin_id_fk` INT NOT NULL,
    `start_time` DATETIME NOT NULL,
    `end_time` DATETIME NOT NULL,
    `status` VARCHAR(255) NOT NULL,
    `created_at` DATETIME NOT NULL,
    PRIMARY KEY(`competition_id_pk`)
);
ALTER TABLE
    `submissions` ADD CONSTRAINT `submissions_team_id_fk_foreign` FOREIGN KEY(`team_id_fk`) REFERENCES `teams`(`team_id_pk`);
ALTER TABLE
    `challenges` ADD CONSTRAINT `challenges_cat_id_fk_foreign` FOREIGN KEY(`cat_id_fk`) REFERENCES `categories`(`cat_id_pk`);
ALTER TABLE
    `challenges` ADD CONSTRAINT `challenges_admin_id_fk_foreign` FOREIGN KEY(`admin_id_fk`) REFERENCES `admins`(`admin_id_pk`);
ALTER TABLE
    `team_members` ADD CONSTRAINT `team_members_player_id_fk_foreign` FOREIGN KEY(`player_id_fk`) REFERENCES `players`(`player_id_pk`);
ALTER TABLE
    `team_members` ADD CONSTRAINT `team_members_team_id_fk_foreign` FOREIGN KEY(`team_id_fk`) REFERENCES `teams`(`team_id_pk`);
ALTER TABLE
    `submissions` ADD CONSTRAINT `submissions_challenge_id_fk_foreign` FOREIGN KEY(`challenge_id_fk`) REFERENCES `challenges`(`challenge_id_pk`);
ALTER TABLE
    `competitions` ADD CONSTRAINT `competitions_admin_id_fk_foreign` FOREIGN KEY(`admin_id_fk`) REFERENCES `admins`(`admin_id_pk`);
ALTER TABLE
    `hints` ADD CONSTRAINT `hints_challenge_id_fk_foreign` FOREIGN KEY(`challenge_id_fk`) REFERENCES `challenges`(`challenge_id_pk`);
ALTER TABLE
    `challenges` ADD CONSTRAINT `challenges_competition_id_fk_foreign` FOREIGN KEY(`competition_id_fk`) REFERENCES `competitions`(`competition_id_pk`);
ALTER TABLE
    `scores` ADD CONSTRAINT `scores_team_id_pfk_foreign` FOREIGN KEY(`team_id_pfk`) REFERENCES `teams`(`team_id_pk`);