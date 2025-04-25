## 1. first create the database:

CREATE DATABASE MarketHub;
USE MarketHub;

CREATE TABLE User (
    userID VARCHAR(10) PRIMARY KEY,
    password VARCHAR(20) NOT NULL
);


CREATE TABLE Supplier (
    userID VARCHAR(10),
    sName VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phoneNo INT NOT NULL,
    FOREIGN KEY (userID) REFERENCES User(userID)
);


CREATE TABLE Customer (
    userID VARCHAR(10),
    cName VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phoneNo INT NOT NULL,
    FOREIGN KEY (userID) REFERENCES User(userID)
);

-- Sample Data for Customer Table
INSERT INTO Customer (userID, cName, email, phoneNo) VALUES
('C001', 'Customer One', 'customer1@example.com', 9998887771),
('C002', 'Customer Two', 'customer2@example.com', 9998887772),
('C003', 'Customer Three', 'customer3@example.com', 9998887773),
('C004', 'Customer Four', 'customer4@example.com', 9998887774),
('C005', 'Customer Five', 'customer5@example.com', 9998887775);

-- Sample Data for Supplier Table
INSERT INTO Supplier (userID, sName, email, phoneNo) VALUES 
('S001', 'Supplier One', 'supplier1@example.com', '9876543210'),
('S002', 'Supplier Two', 'supplier2@example.com', '9876543211'),
('S003', 'Supplier Three', 'supplier3@example.com', '9876543212'),
('S004', 'Supplier Four', 'supplier4@example.com', '9876543213'),
('S005', 'Supplier Five', 'supplier5@example.com', '9876543214');


## 2. make sure you have right credientials in db.py

## 3. open the folder where you have saved app.py and type `python app.py`
