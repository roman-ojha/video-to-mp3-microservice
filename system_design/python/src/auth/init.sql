-- this user is actual user which will access our database not the user trying to give access to api
-- CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Auth123';
-- this is the user that we are creating to access the mysql Database
-- but by default we have the username 'root' with blank password if you want to use that

-- database for auth service
-- CREATE DATABASE video_to_mp3_ms_auth; 

-- granting all the privileges for auth tables to 'auth_user'@'localhost'
-- GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';
-- USE video_to_mp3_ms_auth;

-- creating table
CREATE TABLE user(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- inserting new user to test for our application
INSERT INTO user (email, password) VALUES ('roman@gmail.com', 'Admin123');