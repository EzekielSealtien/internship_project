-- Drop the tables if they already exist
DROP TABLE IF EXISTS doctors;

-- Create the doctors table
CREATE TABLE doctors (
    doctor_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    specialization VARCHAR(100),
    phone_number VARCHAR(15)
);


DROP TABLE IF EXISTS users;

-- Create the users table with a foreign key referencing doctor_id in the doctors table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    date_of_birth DATE,
    phone_number VARCHAR(15),
    doctor_id INTEGER,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

-- Drop the alerts table if it already exists
DROP TABLE IF EXISTS alerts;

-- Create the alerts table
CREATE TABLE alerts (
    alert_id SERIAL PRIMARY KEY,
    alert_type VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'new',
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)


);

-- Drop the health_data table if it already exists
DROP TABLE IF EXISTS health_data;

-- Create the health_data table
CREATE TABLE health_data (
    data_id SERIAL PRIMARY KEY,
    heart_rate INTEGER,
    blood_pressure INTEGER,
    oxygen_level DECIMAL,
    temperature DECIMAL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


