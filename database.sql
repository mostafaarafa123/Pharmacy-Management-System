-- Suppliers Table
CREATE TABLE Suppliers (
    SupplierID INT PRIMARY KEY,
    CompanyName VARCHAR(100) NOT NULL,
    ContactName VARCHAR(50),
    Phone VARCHAR(15) UNIQUE, 
    Address VARCHAR(255)
);

-- Customers Table
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    FullName VARCHAR(100) NOT NULL,
    Phone VARCHAR(15),
    Age INT CHECK (Age > 0) 
);

--  Doctors Table 
CREATE TABLE Doctors (
    DoctorID INT PRIMARY KEY,
    Doctor_Name VARCHAR(100), 
    Specialty VARCHAR(100),
    Phone VARCHAR(20)
);

-- Medicines Table 
CREATE TABLE Medicines (
    MedicineID INT PRIMARY KEY,
    Medicine_Name VARCHAR(100) NOT NULL, 
    Category VARCHAR(50),
    Price DECIMAL(10, 2) CHECK (Price > 0), 
    StockQuantity INT DEFAULT 0,
    ExpiryDate DATE,
    SupplierID INT,
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID)
);

-- Prescriptions Table
CREATE TABLE Prescriptions (
    PrescriptionID INT PRIMARY KEY,
    IssueDate DATE,
    Notes VARCHAR(300),
    CustomerID INT,
    DoctorID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID)
);

-- Orders Table
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    OrderDate DATE,
    TotalAmount DECIMAL(10, 2),
    CustomerID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- OrderDetails Table
CREATE TABLE OrderDetails (
    OrderID INT,
    MedicineID INT,
    Quantity INT CHECK (Quantity > 0),
    LineTotal DECIMAL(10, 2), 
    PRIMARY KEY (OrderID, MedicineID), 
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (MedicineID) REFERENCES Medicines(MedicineID)
);

-- Suppliers
INSERT INTO Suppliers (SupplierID, CompanyName, ContactName, Phone, Address) VALUES 
(1, 'PharmaEgy', 'Dr. Hassan', '01011111111', 'Cairo, Downtown'),
(2, 'GlobalMeds', 'Dr. Sarah', '01222222222', 'Alexandria, Smouha'),
(3, 'Nile Pharmaceuticals', 'Dr. Tarek', '01133333333', 'Giza, Dokki'),
(4, 'Upper Egypt Medical', 'Dr. Youssef', '01544444444', 'Assiut'),
(5, 'Cairo Import Co', 'Dr. Mona', '01055555555', 'Nasr City, Cairo');

-- Customers
INSERT INTO Customers (CustomerID, FullName, Phone, Age) VALUES 
(101, 'Ahmed Ali', '01012345678', 30),
(102, 'Mona Zaki', '01123456789', 25),
(103, 'Khaled Said', '01234567890', 45),
(104, 'Sara Mahmoud', '01545678901', 22),
(105, 'Omar Hassan', '01098765432', 60), 
(106, 'Laila Ezz', '01187654321', 35),
(107, 'Mostafa Kamel', '01276543210', 50),
(108, 'Hanan Youssef', '01565432109', 28),
(109, 'Karim Wael', '01011223344', 19),
(110, 'Yara Samy', '01299887766', 31);

-- Doctors 
INSERT INTO Doctors (DoctorID, Doctor_Name, Specialty, Phone) VALUES 
(1, 'Dr. Magdy Yacoub', 'Cardiology', '0100000001'),
(2, 'Dr. Hisham Barakat', 'Internal Medicine', '0100000002'),
(3, 'Dr. Sherif Fayed', 'ENT', '0100000003'),
(4, 'Dr. Mona Mina', 'Orthopedics', '0100000004'),
(5, 'Dr. Ahmed Zewail', 'General', '0100000005');

-- Medicines 
INSERT INTO Medicines (MedicineID, Medicine_Name, Category, Price, StockQuantity, ExpiryDate, SupplierID) VALUES 
(1, 'Panadol Extra', 'Painkiller', 45.00, 100, '2026-12-30', 1),
(2, 'Augmentin 1g', 'Antibiotic', 120.00, 50, '2025-05-20', 1),
(3, 'Omega3 Plus', 'Supplement', 200.00, 20, '2024-10-01', 2), 
(4, 'Concor 5mg', 'Heart', 60.00, 80, '2027-01-15', 3),
(5, 'Glucophage 1000', 'Diabetes', 40.00, 90, '2026-11-01', 3),
(6, 'Cataflam 50mg', 'Painkiller', 35.00, 60, '2026-08-10', 1),
(7, 'Zithromax', 'Antibiotic', 85.00, 40, '2025-12-01', 2),
(8, 'Otrivin Adult', 'Nasal Spray', 25.00, 150, '2026-06-30', 4),
(9, 'Voltaren Gel', 'Topical', 45.00, 30, '2027-02-28', 2),
(10, 'Centrum', 'Vitamin', 350.00, 25, '2026-09-15', 5),
(11, 'Aspirin Protect', 'Blood Thinner', 15.00, 200, '2025-07-20', 3),
(12, 'Antinal', 'Digestive', 20.00, 100, '2028-01-01', 4),
(13, 'Nexium 40mg', 'Gastric', 110.00, 45, '2026-03-10', 2),
(14, 'Bepanthen', 'Skincare', 65.00, 70, '2027-05-05', 5),
(15, 'Insulin Mixtard', 'Diabetes', 150.00, 15, '2025-04-01', 1);

-- Prescriptions
INSERT INTO Prescriptions (PrescriptionID, IssueDate, Notes, CustomerID, DoctorID) VALUES 
(1, '2025-10-01', 'Take Concor daily in the morning', 105, 1), 
(2, '2025-10-05', 'Glucophage twice a day after meals', 105, 2), 
(3, '2025-10-10', 'Augmentin every 12 hours for 7 days', 102, 3), 
(4, '2025-10-12', 'Voltaren Gel twice daily for back pain', 107, 4),
(5, '2025-10-15', 'Vitamin C and Zinc for immunity', 109, 5);

-- Orders & OrderDetails
INSERT INTO Orders VALUES (5001, '2025-10-01', 45.00, 101);
INSERT INTO OrderDetails VALUES (5001, 1, 1, 45.00);

INSERT INTO Orders VALUES (5002, '2025-10-02', 155.00, 102);
INSERT INTO OrderDetails VALUES (5002, 2, 1, 120.00); 
INSERT INTO OrderDetails VALUES (5002, 6, 1, 35.00);  

INSERT INTO Orders VALUES (5003, '2025-10-03', 700.00, 103);
INSERT INTO OrderDetails VALUES (5003, 10, 2, 700.00); 

INSERT INTO Orders VALUES (5004, '2025-10-05', 100.00, 105);
INSERT INTO OrderDetails VALUES (5004, 4, 1, 60.00); 
INSERT INTO OrderDetails VALUES (5004, 5, 1, 40.00);  

INSERT INTO Orders VALUES (5005, '2025-10-06', 130.00, 104);
INSERT INTO OrderDetails VALUES (5005, 14, 2, 130.00);

INSERT INTO Orders VALUES (5006, '2025-10-07', 45.00, 106);
INSERT INTO OrderDetails VALUES (5006, 8, 1, 25.00); 
INSERT INTO OrderDetails VALUES (5006, 12, 1, 20.00); 

INSERT INTO Orders VALUES (5007, '2025-10-08', 220.00, 108);
INSERT INTO OrderDetails VALUES (5007, 13, 2, 220.00); 

INSERT INTO Orders VALUES (5008, '2025-10-09', 45.00, 109);
INSERT INTO OrderDetails VALUES (5008, 9, 1, 45.00); 

INSERT INTO Orders VALUES (5009, '2025-10-10', 95.00, 110);
INSERT INTO OrderDetails VALUES (5009, 1, 1, 45.00);  
INSERT INTO OrderDetails VALUES (5009, 12, 1, 20.00); 
INSERT INTO OrderDetails VALUES (5009, 11, 2, 30.00); 

INSERT INTO Orders VALUES (5010, '2025-10-12', 300.00, 101);
INSERT INTO OrderDetails VALUES (5010, 15, 2, 300.00); 

-- Ali saad 202403246

-- Increase the price of all antibiotics by 10%
 UPDATE Medicines SET Price = Price * 1.10 WHERE Category = 'Antibiotic';

-- Set stock to zero for damaged/expired medicine
 UPDATE Medicines SET StockQuantity = 0 WHERE MedicineID = 3;

--  Insert a customer without a phone number
 INSERT INTO Customers (CustomerID, FullName, Age) VALUES (112, 'Test User', 40);

-- Delete an item from an invoice
 DELETE FROM OrderDetails WHERE OrderID = 5001 AND MedicineID = 1;

-- Move a medicine to another supplier
 UPDATE Medicines SET SupplierID = 2 WHERE MedicineID = 5;

-- Add a note to a prescription
 UPDATE Prescriptions SET Notes = 'Urgent Case' WHERE PrescriptionID = 2;

 -- Join Medicine and Supplier names
SELECT M.Medicine_Name, S.CompanyName FROM Medicines M JOIN Suppliers S ON M.SupplierID = S.SupplierID;

-- Join Customer names and their order dates
SELECT C.FullName, O.OrderDate FROM Customers C JOIN Orders O ON C.CustomerID = O.CustomerID;

-- Get full Order Details (ID, Medicine Name, Quantity, Price)
SELECT O.OrderID, M.Medicine_Name, D.Quantity, D.LineTotal 
FROM OrderDetails D 
JOIN Medicines M ON D.MedicineID = M.MedicineID 
JOIN Orders O ON D.OrderID = O.OrderID;

-- List customers and their doctor's name
SELECT C.FullName, D.Doctor_Name 
FROM Customers C 
JOIN Prescriptions P ON C.CustomerID = P.CustomerID
JOIN Doctors D ON P.DoctorID = D.DoctorID;


-- Abdallah Hesham 202400592

-- Select all medicines
SELECT * FROM Medicines;

-- Find medicines that have NEVER been sold (Left Join)
SELECT M.Medicine_Name FROM Medicines M LEFT JOIN OrderDetails D ON M.MedicineID = D.MedicineID WHERE D.OrderID IS NULL;

-- Find suppliers who haven't supplied any active medicine
SELECT S.CompanyName FROM Suppliers S LEFT JOIN Medicines M ON S.SupplierID = M.SupplierID WHERE M.MedicineID IS NULL;

-- Report total amount paid by each customer
SELECT C.FullName, SUM(O.TotalAmount) AS TotalPaid
FROM Customers C JOIN Orders O ON C.CustomerID = O.CustomerID GROUP BY C.FullName;

-- List names of medicines sold on a specific day (25-10)
SELECT DISTINCT M.Medicine_Name 
FROM Medicines M JOIN OrderDetails D ON M.MedicineID = D.MedicineID JOIN Orders O ON D.OrderID = O.OrderID 
WHERE O.OrderDate = '2025-10-25';

-- Select medicines with stock between 10 and 50
SELECT * FROM Medicines WHERE StockQuantity BETWEEN 10 AND 50;

-- Select distinct doctor names from prescriptions
SELECT DISTINCT D.Doctor_Name
FROM Prescriptions P
JOIN Doctors D ON P.DoctorID = D.DoctorID;

-- Select suppliers who do not have a phone number
SELECT * FROM Suppliers WHERE Phone IS NULL;

-- Select medicines from specific categories
SELECT * FROM Medicines WHERE Category IN ('Painkiller', 'Antibiotic');

-- Select customers younger than 20
SELECT * FROM Customers WHERE Age < 20;


-- Omar mahmoud 202401118

-- Order customers alphabetically
SELECT * FROM Customers ORDER BY FullName ASC;

--  Order medicines by expiry date (Soonest first)
SELECT * FROM Medicines ORDER BY ExpiryDate ASC;

-- Count total registered customers
SELECT COUNT(*) AS CustomerCount FROM Customers;

-- Calculate average price of medicines
SELECT AVG(Price) AS AveragePrice FROM Medicines;

-- Find the most expensive medicine
SELECT MAX(Price) AS MaxPrice FROM Medicines;

-- Find the minimum stock quantity available
SELECT MIN(StockQuantity) AS MinStock FROM Medicines;

--  Calculate total revenue (sum of all orders)
SELECT SUM(TotalAmount) AS TotalRevenue FROM Orders;

-- Count number of medicines in each category
SELECT Category, COUNT(*) AS Count FROM Medicines GROUP BY Category;

--  Calculate total stock quantity for each supplier
SELECT SupplierID, SUM(StockQuantity) AS TotalStock FROM Medicines GROUP BY SupplierID;

--  Count number of prescriptions per doctor
SELECT D.Doctor_Name, COUNT(*) AS ScriptCount 
FROM Prescriptions P 
JOIN Doctors D ON P.DoctorID = D.DoctorID 
GROUP BY D.Doctor_Name;


-- Mostafa Tayel 202402876

-- Show supplier details for each sold medicine
SELECT D.OrderID, M.Medicine_Name, S.CompanyName 
FROM OrderDetails D JOIN Medicines M ON D.MedicineID = M.MedicineID JOIN Suppliers S ON M.SupplierID = S.SupplierID;

--  Identify "Stagnant Medicines" (Subquery with NOT IN)
SELECT Medicine_Name, StockQuantity, Price
FROM Medicines
WHERE MedicineID NOT IN (SELECT DISTINCT MedicineID FROM OrderDetails)
AND StockQuantity > 0;

--  Top 3 Customers (Highest Spenders)
SELECT TOP 3 C.FullName, SUM(O.TotalAmount) AS TotalSpent
FROM Customers C
JOIN Orders O ON C.CustomerID = O.CustomerID
GROUP BY C.FullName
ORDER BY TotalSpent DESC;

-- Medicines generating revenue above average (Having with Subquery)
SELECT M.Medicine_Name, SUM(D.LineTotal) AS TotalRevenue
FROM Medicines M
JOIN OrderDetails D ON M.MedicineID = D.MedicineID
GROUP BY M.Medicine_Name
HAVING SUM(D.LineTotal) > (SELECT AVG(LineTotal) FROM OrderDetails);

--  The "Golden Supplier" (Supplier generating most revenue)
SELECT TOP 1 S.CompanyName, SUM(D.LineTotal) AS RevenueGenerated
FROM Suppliers S
JOIN Medicines M ON S.SupplierID = M.SupplierID
JOIN OrderDetails D ON M.MedicineID = D.MedicineID
GROUP BY S.CompanyName
ORDER BY RevenueGenerated DESC;

-- Customers who bought ONLY 'Antibiotics'
SELECT DISTINCT C.FullName
FROM Customers C
JOIN Orders O ON C.CustomerID = O.CustomerID
JOIN OrderDetails D ON O.OrderID = D.OrderID
JOIN Medicines M ON D.MedicineID = M.MedicineID
WHERE M.Category = 'Antibiotic';

-- Cumulative Sales Report 
SELECT 
    OrderID, 
    OrderDate, 
    TotalAmount, 
    SUM(TotalAmount) OVER (ORDER BY OrderDate, OrderID) AS RunningTotal
FROM Orders;

-- Increase price by 20% for low stock items
UPDATE Medicines SET Price = Price * 1.20 WHERE StockQuantity < 10 AND StockQuantity > 0;

-- "Dormant" Customers (No purchases in last 30 days)
SELECT FullName, Phone 
FROM Customers 
WHERE CustomerID NOT IN (
    SELECT CustomerID FROM Orders 
    WHERE OrderDate >= DATEADD(day, -30, GETDATE())
);

-- The most expensive invoice for each customer
SELECT C.FullName, O.OrderID, O.TotalAmount
FROM Customers C
JOIN Orders O ON C.CustomerID = O.CustomerID
WHERE O.TotalAmount = (
    SELECT MAX(TotalAmount) 
    FROM Orders 
    WHERE CustomerID = C.CustomerID
);

--  Compare current medicine price vs price at time of sale
SELECT D.OrderID, M.Medicine_Name, D.LineTotal, M.Price 
FROM OrderDetails D JOIN Medicines M ON D.MedicineID = M.MedicineID;
