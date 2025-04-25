CREATE DATABASE school_db;

USE school_db;

CREATE TABLE Teacher (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100)
);

CREATE TABLE Student (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    class VARCHAR(10),
    dob DATE,
    address TEXT
);

INSERT INTO Teacher (name, email, password) VALUES 
('Anjali Mehta', 'anjali.mehta@school.com', 'pass123'),
('Rajesh Kumar', 'rajesh.kumar@school.com', 'rajesh456'),
('Priya Sharma', 'priya.sharma@school.com', 'priya789'),
('Amitabh Verma', 'amitabh.verma@school.com', 'amitpass'),
('Neha Reddy', 'neha.reddy@school.com', 'neha321'),
('Suresh Iyer', 'suresh.iyer@school.com', 'iyerpass'),
('Kavita Joshi', 'kavita.joshi@school.com', 'kavita007'),
('Vikram Desai', 'vikram.desai@school.com', 'desai999'),
('Shalini Nair', 'shalini.nair@school.com', 'nair000'),
('Manoj Bhatia', 'manoj.bhatia@school.com', 'manoj432');


INSERT INTO Student (name, email, password, class, dob, address) VALUES 
('Rohan Gupta', 'rohan.gupta@student.com', 'rohan123', '10A', '2009-05-14', 'Delhi, India'),
('Sneha Patel', 'sneha.patel@student.com', 'sneha456', '9B', '2010-08-23', 'Ahmedabad, Gujarat'),
('Arjun Reddy', 'arjun.reddy@student.com', 'arjun789', '11C', '2008-03-17', 'Hyderabad, Telangana'),
('Isha Singh', 'isha.singh@student.com', 'isha321', '8A', '2011-11-12', 'Lucknow, Uttar Pradesh'),
('Karan Das', 'karan.das@student.com', 'karan654', '12B', '2007-02-05', 'Kolkata, West Bengal'),
('Meera Iyer', 'meera.iyer@student.com', 'meera999', '7C', '2012-07-30', 'Chennai, Tamil Nadu'),
('Tanishq Roy', 'tanishq.roy@student.com', 'tanishq000', '9A', '2010-10-19', 'Mumbai, Maharashtra'),
('Divya Nair', 'divya.nair@student.com', 'divya777', '10B', '2009-04-03', 'Kochi, Kerala'),
('Yash Mehta', 'yash.mehta@student.com', 'yash852', '11A', '2008-09-25', 'Surat, Gujarat'),
('Pooja Chauhan', 'pooja.chauhan@student.com', 'pooja963', '8B', '2011-01-18', 'Jaipur, Rajasthan');

