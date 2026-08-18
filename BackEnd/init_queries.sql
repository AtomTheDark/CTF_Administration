DROP DATABASE IF EXISTS ctf;
CREATE DATABASE IF NOT EXISTS ctf;
USE ctf;

CREATE TABLE admins(
    admin_id_pk INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(75) NOT NULL,
    email VARCHAR(75) NOT NULL,
    admin_password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL
);
CREATE TABLE competitions(
    competition_id_pk int PRIMARY KEY,
    competition_name VARCHAR(75) NOT NULL,
    competition_description VARCHAR(255),
    admin_id_fk INT NOT NULL,
    start_time DATETIME,
    end_time DATETIME,
    competition_status VARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(admin_id_fk) REFERENCES admins(admin_id_pk)
);
CREATE TABLE players(
    player_id_pk INT PRIMARY KEY,
    player_name VARCHAR(50) NOT NULL,
    player_username VARCHAR(200) NOT NULL,
    player_passwd_hash VARCHAR(255)
);
CREATE TABLE teams(
    team_id_pk INT PRIMARY KEY,
    team_name VARCHAR(75)
);
CREATE TABLE team_members(
    team_id_cpfk INT,
    player_id_cpfk INT,
    PRIMARY KEY(team_id_cpfk,player_id_cpfk),
    FOREIGN KEY(team_id_cpfk) REFERENCES teams(team_id_pk),
    FOREIGN KEY(player_id_cpfk) REFERENCES players(player_id_pk)
);
CREATE TABLE scores(
    team_id_pfk INT AUTO_INCREMENT PRIMARY KEY,
    total_points INT,
    challenges_solved INT,
    FOREIGN KEY(team_id_pfk) REFERENCES teams(team_id_pk)
);
CREATE TABLE categories(
    cat_id_pk INT AUTO_INCREMENT PRIMARY KEY,
    cat_name VARCHAR(75)
);
CREATE TABLE challenges(
    challenge_id_pk INT AUTO_INCREMENT PRIMARY KEY,
    competition_id_fk INT NOT NULL,
    title VARCHAR(50),
    challenge_description VARCHAR(255),
    cat_id_fk INT NOT NULL,
    difficulty VARCHAR(25),
    points INT NOT NULL,
    hashed_flag VARCHAR(255),
    admin_id_fk INT NOT NULL,
    created_at DATETIME,
    FOREIGN KEY(competition_id_fk) REFERENCES competitions(competition_id_pk),
    FOREIGN KEY(cat_id_fk) REFERENCES categories(cat_id_pk),
    FOREIGN KEY(admin_id_fk) REFERENCES admins(admin_id_pk)
);
CREATE TABLE hints(
    hint_id INT AUTO_INCREMENT PRIMARY KEY,
    challenge_id_fk INT NOT NULL,
    hint_text TEXT NOT NULL,
    cost INT NOT NULL,
    FOREIGN KEY(challenge_id_fk) REFERENCES challenges(cat_id_fk)
);
CREATE TABLE submissions(
    submission_id INT AUTO_INCREMENT PRIMARY KEY,
    team_id_fk INT,
    challenge_id_fk INT,
    submitted_flag VARCHAR(255),
    submitted_flag_hash VARCHAR(255),
    is_correct BOOLEAN NOT NULL,
    submited_at DATETIME NOT NULL,
    FOREIGN KEY(team_id_fk) REFERENCES teams(team_id_pk),
    FOREIGN KEY(challenge_id_fk) REFERENCES challenges(challenge_id_pk)
);