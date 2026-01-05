-- Database Creation
CREATE DATABASE IF NOT EXISTS event_system_db;
USE event_system_db;

-- Drop Tables if exist (Cleanup)
DROP VIEW IF EXISTS v_upcoming_events;
DROP VIEW IF EXISTS v_revenue_report;
DROP TABLE IF EXISTS booking_items;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS venues;

-- 1. Venues Table
CREATE TABLE venues (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    capacity INT NOT NULL
);

-- 2. Users Table (Enum Requirement)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'customer') NOT NULL DEFAULT 'customer',
    display_name VARCHAR(100)
);

-- 3. Events Table (Float, Bool, DateTime Requirements)
CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venue_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    start_time DATETIME NOT NULL,
    base_price FLOAT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (venue_id) REFERENCES venues(id)
);

-- 4. Bookings Table
CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_price FLOAT NOT NULL,
    status ENUM('confirmed', 'cancelled') DEFAULT 'confirmed',
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 5. Booking Items (M:N Relationship between Bookings and Events)
CREATE TABLE booking_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    event_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price FLOAT NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(id)
);

-- View 1: Active Upcoming Events
CREATE VIEW v_upcoming_events AS
SELECT 
    e.id, 
    e.title, 
    e.start_time, 
    e.base_price, 
    v.name AS venue_name,
    v.address AS venue_address
FROM events e
JOIN venues v ON e.venue_id = v.id
WHERE e.is_active = TRUE AND e.start_time > NOW();

-- View 2: Revenue Report (Aggregated Data)
CREATE VIEW v_revenue_report AS
SELECT 
    e.id AS event_id,
    e.title,
    COUNT(bi.id) AS total_tickets_sold,
    COALESCE(SUM(bi.quantity * bi.unit_price), 0) AS total_revenue
FROM events e
LEFT JOIN booking_items bi ON e.id = bi.event_id
LEFT JOIN bookings b ON bi.booking_id = b.id
WHERE b.status = 'confirmed' OR b.status IS NULL
GROUP BY e.id, e.title;

-- Seed Data (Optional, for initial testing)
INSERT INTO venues (name, address, capacity) VALUES 
('Main Hall', '123 Main St', 100),
('Small Club', '45 Side St', 50);

INSERT INTO users (email, password_hash, role, display_name) VALUES 
('admin@test.com', 'hashed_secret', 'admin', 'Admin User'),
('customer@test.com', 'hashed_secret', 'customer', 'John Doe');
