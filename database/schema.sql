-- AI-Powered Career Recommendation System
-- Database Schema

CREATE DATABASE IF NOT EXISTS career_db;
USE career_db;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    gpa FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Profiles Table
CREATE TABLE IF NOT EXISTS user_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    python_skill INT NOT NULL,       -- 0 to 10
    ml_skill INT NOT NULL,
    web_skill INT NOT NULL,
    database_skill INT NOT NULL,
    aptitude_score INT NOT NULL,     -- 0 to 100
    interest VARCHAR(100) NOT NULL,  -- e.g. "Data Science"
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Career Roles Table
CREATE TABLE IF NOT EXISTS career_roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(100) NOT NULL,
    demand_level VARCHAR(20) NOT NULL  -- High / Medium / Low
);

-- Recommendations Table
CREATE TABLE IF NOT EXISTS recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    career_role VARCHAR(100) NOT NULL,
    match_score FLOAT NOT NULL,
    demand_level VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Insert Sample Career Roles
INSERT INTO career_roles (role_name, demand_level) VALUES
('Data Scientist', 'High'),
('ML Engineer', 'High'),
('Data Analyst', 'Medium'),
('Cybersecurity Analyst', 'Medium'),
('Software Developer', 'High');
