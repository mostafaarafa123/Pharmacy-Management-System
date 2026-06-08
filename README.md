#  Pharmacy Smart System

A comprehensive Pharmacy Management System designed to streamline pharmacy operations, including inventory control, point-of-sale (POS) processing, customer/doctor management, and prescription tracking.

##  Key Features

* ** Smart Dashboard:** Real-time metrics on revenue, inventory status, and low-stock alerts.
* ** Intelligent POS System:** Real-time cart management with automatic inventory updates upon order confirmation.
* ** Inventory Management:** Supports adding, updating, and "Soft Archiving" of medicines to maintain historical data integrity.
* ** Database-Driven Entities:** Full CRUD operations for Customers, Doctors, and Suppliers.
* ** Prescription Tracking:** Links patients and doctors to specific medical notes and history.

##  Technical Stack

* **Frontend:** [Streamlit] (Interactive Dashboard)
* **Database Engine:** Microsoft SQL Server
* **Connectivity:** `pyodbc` for robust database communication
* **Data Analysis:** `pandas` for querying and data visualization

##  Database Schema & Analytics
The system relies on a normalized relational database schema involving:
- **Relational Tables:** Suppliers, Medicines, Customers, Doctors, Prescriptions, Orders, and OrderDetails.
- **Advanced SQL:** Includes complex queries such as:
    - **Aggregate Reporting:** Sales trends and cumulative revenue tracking.
    - **Business Intelligence:** Identifying stagnant medicines, top-spending customers, and high-revenue suppliers.
    - **Data Integrity:** Using `JOINs`, `GROUP BY`, `HAVING`, and window functions for analytical reporting.

##  How to Run

1. **Prerequisites:** Ensure you have Microsoft SQL Server installed and the database `inventory_system` configured.
2. **Setup Connection:** Update the `SERVER_NAME` variable in `main.py` to match your local SQL Server instance.
3. **Install Dependencies:**
   ```bash
   pip install streamlit pyodbc pandas
