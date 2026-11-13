-- Trek With Me Database Schema
-- Run this in MySQL to set up the database

CREATE DATABASE IF NOT EXISTS trek_with_me;
USE trek_with_me;

-- Users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role ENUM('user','admin') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Treks
CREATE TABLE IF NOT EXISTS treks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    location VARCHAR(150),
    description TEXT,
    difficulty ENUM('Easy','Moderate','Hard','Expert') DEFAULT 'Moderate',
    duration_days INT DEFAULT 1,
    price DECIMAL(10,2) DEFAULT 0,
    image_url VARCHAR(300),
    latitude DECIMAL(10,6) DEFAULT 0,
    longitude DECIMAL(10,6) DEFAULT 0,
    max_altitude VARCHAR(50),
    rating DECIMAL(3,1) DEFAULT 4.0,
    is_active TINYINT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Homestays
CREATE TABLE IF NOT EXISTS homestays (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trek_id INT,
    name VARCHAR(150),
    description TEXT,
    price_per_night DECIMAL(10,2),
    image_url VARCHAR(300),
    is_active TINYINT DEFAULT 1,
    FOREIGN KEY (trek_id) REFERENCES treks(id)
);

-- Bookings
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    trek_id INT,
    trek_date DATE,
    num_people INT DEFAULT 1,
    homestay_id INT NULL,
    total_amount DECIMAL(10,2),
    payment_status ENUM('pending','paid','cancelled') DEFAULT 'pending',
    payment_method VARCHAR(50) DEFAULT 'upi',
    payment_reference VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (trek_id) REFERENCES treks(id)
);

-- If you are updating an existing database, run these alter statements:
-- ALTER TABLE bookings ADD COLUMN payment_method VARCHAR(50) DEFAULT 'upi';
-- ALTER TABLE bookings ADD COLUMN payment_reference VARCHAR(100) NULL;
-- ALTER TABLE sos_alerts ADD COLUMN landmark VARCHAR(255) NULL;

-- SOS Alerts
CREATE TABLE IF NOT EXISTS sos_alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    message TEXT,
    landmark VARCHAR(255) NULL,
    admin_message TEXT NULL,
    status ENUM('active','resolved') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Contacts
CREATE TABLE IF NOT EXISTS contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Feedback
CREATE TABLE IF NOT EXISTS feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ─── SEED DATA ───────────────────────────────────────────

INSERT INTO users (name, email, password, role) VALUES
('Admin', 'admin@trekwithme.com', SHA2('admin123', 256), 'admin'),
('John Hiker', 'john@example.com', SHA2('pass123', 256), 'user');

INSERT INTO treks (name, location, description, difficulty, duration_days, price, image_url, latitude, longitude, max_altitude, rating) VALUES
('Roopkund Lake Trek', 'Uttarakhand, India', 'A high-altitude glacial lake trek surrounded by the bones of ancient pilgrims and breathtaking Himalayan panoramas.', 'Hard', 8, 12500.00, 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800', 30.2493, 79.7316, '5029m', 4.8),
('Valley of Flowers', 'Chamoli, Uttarakhand', 'UNESCO World Heritage site — a mesmerizing valley bursting with endemic alpine flowers and rich biodiversity.', 'Moderate', 6, 9500.00, 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800', 30.7280, 79.6059, '3658m', 4.9),
('Kedarkantha Summit', 'Uttarkashi, Uttarakhand', 'One of the best winter treks in India with stunning 360° views of Himalayan peaks from the summit.', 'Moderate', 6, 8000.00, 'https://images.unsplash.com/photo-1454496522488-7a8e488e8606?w=800', 31.0205, 78.1561, '3810m', 4.7),
('Hampta Pass Crossing', 'Kullu, Himachal Pradesh', 'A dramatic crossover from lush Kullu valley to the stark Lahaul landscape — two worlds in one trek.', 'Moderate', 5, 9000.00, 'https://images.unsplash.com/photo-1501854140801-50d01698950b?w=800', 32.2396, 77.2590, '4270m', 4.6),
('Chadar Frozen River Trek', 'Ladakh', 'Walk on the frozen Zanskar River in winter — one of the most extreme and surreal adventures on Earth.', 'Expert', 9, 22000.00, 'https://images.unsplash.com/photo-1551632811-561732d1e306?w=800', 33.7782, 77.5619, '3200m', 4.9),
('Triund Ridge Trek', 'Dharamshala, HP', 'A stunning short trek above Dharamshala with gorgeous views of the Kangra valley and Dhauladhar range.', 'Easy', 2, 3500.00, 'https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5?w=800', 32.2432, 76.3234, '2827m', 4.5),
('Sandakphu Peak Trek', 'Darjeeling, West Bengal', 'The highest peak in West Bengal offering rare simultaneous views of four of the world\'s five highest peaks.', 'Hard', 7, 11000.00, 'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=800', 27.1068, 88.0009, '3636m', 4.7),
('Chopta Tungnath Trek', 'Rudraprayag, Uttarakhand', 'Home to the world\'s highest Shiva temple and a gateway to Chandrashila summit with panoramic Himalayan views.', 'Easy', 3, 5500.00, 'https://images.unsplash.com/photo-1544085701-4d1d2b1d2a5d?w=800', 30.4922, 79.2195, '4090m', 4.6);

INSERT INTO homestays (trek_id, name, description, price_per_night, image_url) VALUES
(1, 'Mountain Nest Homestay', 'Cozy wooden cottage with fireplace and mountain views.', 1200.00, 'https://images.unsplash.com/photo-1510798831971-661eb04b3739?w=600'),
(2, 'Valley View Homestay', 'Traditional Garhwali home with home-cooked meals included.', 900.00, 'https://images.unsplash.com/photo-1449158743715-0a90ebb6d2d8?w=600'),
(3, 'Pine Ridge Stay', 'Comfortable stay surrounded by dense pine forests.', 800.00, 'https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=600'),
(6, 'Himalayan Hearth', 'Budget-friendly stay with stunning valley views.', 600.00, 'https://images.unsplash.com/photo-1506197603052-3cc9c3a201bd?w=600');
