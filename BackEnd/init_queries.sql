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