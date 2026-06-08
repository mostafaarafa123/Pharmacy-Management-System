import streamlit as st
import pyodbc
import pandas as pd
from datetime import date

SERVER_NAME = 'DESKTOP-546CUG1'
DATABASE_NAME = 'inventory_system'

def get_connection():
    try:
        conn_str = (
            f'DRIVER={{SQL Server}};'
            f'SERVER={SERVER_NAME};'
            f'DATABASE={DATABASE_NAME};'
            'Trusted_Connection=yes;'
        )
        return pyodbc.connect(conn_str)
    except Exception as e:
        st.error(f"❌ Connection Error: {e}")
        return None

if 'cart' not in st.session_state:
    st.session_state.cart = []

def add_to_cart(med_id, med_name, price, qty):
    for item in st.session_state.cart:
        if item['MedicineID'] == med_id:
            item['Quantity'] += qty
            item['LineTotal'] = item['Quantity'] * price
            st.toast(f"Updated: {med_name}", icon="🔄")
            return
    st.session_state.cart.append({
        'MedicineID': med_id, 'Medicine_Name': med_name, 'Price': price, 'Quantity': qty, 'LineTotal': price * qty
    })
    st.toast(f"Added: {med_name}", icon="✅")

def clear_cart():
    st.session_state.cart = []

# Main Layout & Navigation

st.set_page_config(page_title="Pharmacy Smart System", layout="wide", page_icon="🏥")

st.sidebar.title("Pharmacy System")
st.sidebar.markdown("---")
page = st.sidebar.radio("Main Menu:",
                        ["Dashboard", "POS (Sales)", "Inventory (Items)", "Customers", "Doctors", "Suppliers",
                         "Prescriptions"])

# --- DASHBOARD ---
if page == "Dashboard":
    st.title("📊 Dashboard")
    conn = get_connection()
    if conn:
        c1, c2, c3, c4 = st.columns(4)
        sales = pd.read_sql("SELECT ISNULL(SUM(TotalAmount), 0) FROM Orders", conn).iloc[0, 0]
        c1.metric("Revenue", f"{sales:,.0f} EGP")
        c2.metric("Medicines", pd.read_sql("SELECT COUNT(*) FROM Medicines", conn).iloc[0, 0])
        c3.metric("Customers", pd.read_sql("SELECT COUNT(*) FROM Customers", conn).iloc[0, 0])
        c4.metric("Doctors", pd.read_sql("SELECT COUNT(*) FROM Doctors", conn).iloc[0, 0])

        st.divider()
        st.subheader("⚠️ Low Stock Alert")
        st.dataframe(pd.read_sql("SELECT Medicine_Name, StockQuantity FROM Medicines WHERE StockQuantity < 10", conn),
                     use_container_width=True)
        st.divider()
        st.subheader("📅 Daily Sales Overview")
        # This calculates how many orders and how much money was made per day
        query_daily = """
                SELECT 
                    OrderDate, 
                    COUNT(OrderID) as [Orders Count], 
                    SUM(TotalAmount) as [Total Revenue]
                FROM Orders
                GROUP BY OrderDate
                ORDER BY OrderDate DESC
                """
        df_daily = pd.read_sql(query_daily, conn)
        col_table, col_chart = st.columns([1, 2])
        with col_table:
            st.caption("📋 Data Table")
            st.dataframe(df_daily, use_container_width=True)
        with col_chart:
            st.caption("📈 Revenue Trend")
            if not df_daily.empty:
                chart_data = df_daily.set_index("OrderDate")
                st.bar_chart(chart_data['Total Revenue'], color="#4CAF50")
            else:
                st.info("No sales data available yet.")
        conn.close()

# --- POS
elif page == "POS (Sales)":
    st.title("🛒 Point of Sale")
    conn = get_connection()
    if conn:
        customers = pd.read_sql("SELECT CustomerID, FullName FROM Customers", conn)
        medicines = pd.read_sql("SELECT MedicineID, Medicine_Name, Price, StockQuantity FROM Medicines WHERE StockQuantity > 0",
                                conn)
        if customers.empty or medicines.empty:
            st.warning("⚠️ Please add Customers and Medicines first.")
        else:
            c1, c2 = st.columns([2, 1])
            cust_name = c1.selectbox("Customer", customers['FullName'])
            cust_id = customers[customers['FullName'] == cust_name]['CustomerID'].iloc[0]
            order_date = c2.date_input("Date", date.today())
            st.markdown("---")
            c_prod, c_qty, c_add = st.columns([3, 1, 1])
            # Show Stock in Dropdown
            med_list = [f"{r['Medicine_Name']} | {r['Price']} EGP (Stock: {r['StockQuantity']})" for i, r in
                        medicines.iterrows()]
            med_choice = c_prod.selectbox("Product", med_list)
            sel_med = medicines.iloc[med_list.index(med_choice)]
            qty = c_qty.number_input("Qty", 1, int(sel_med['StockQuantity']), 1)
            if c_add.button("Add ➕", use_container_width=True):
                add_to_cart(sel_med['MedicineID'], sel_med['Medicine_Name'], float(sel_med['Price']), qty)
            if st.session_state.cart:
                st.subheader("Current Cart")
                df_cart = pd.DataFrame(st.session_state.cart)
                st.dataframe(df_cart, use_container_width=True)
                total = df_cart['LineTotal'].sum()
                st.success(f"Total: {total:,.2f} EGP")
                c_conf, c_clr = st.columns([3, 1])
                if c_conf.button("✅ Confirm Order", type="primary"):
                    try:
                        cur = conn.cursor()
                        oid = cur.execute("SELECT ISNULL(MAX(OrderID), 5000) + 1 FROM Orders").fetchval()
                        cur.execute("INSERT INTO Orders VALUES (?, ?, ?, ?)",
                                    (oid, str(order_date), total, int(cust_id)))
                        for item in st.session_state.cart:
                            # 1. Convert numpy types to python native types
                            m_id = int(item['MedicineID'])
                            m_qty = int(item['Quantity'])
                            m_total = float(item['LineTotal'])

                            # 2. Execute Queries with clean variables
                            cur.execute("INSERT INTO OrderDetails VALUES (?, ?, ?, ?)",
                                        (int(oid), m_id, m_qty, m_total))

                            cur.execute("UPDATE Medicines SET StockQuantity = StockQuantity - ? WHERE MedicineID = ?",
                                        (m_qty, m_id))
                        conn.commit()
                        st.balloons()
                        st.success("Order Saved!");
                        clear_cart();
                        st.rerun()
                    except Exception as e:
                        st.error(e)
                if c_clr.button("Clear"): clear_cart(); st.rerun()
        conn.close()

# AUTO-FILL SECTIONS (Inventory, Customers, Doctors, Suppliers)

# --- INVENTORY ---
elif page == "Inventory (Items)":
    st.title("💊 Inventory Management")
    conn = get_connection()
    if conn:
        st.info("💡 Enter ID: If it exists, data will auto-load for editing.")
        with st.container(border=True):
            # 1. ID Input first
            m_id = st.number_input("Medicine ID", min_value=1, step=1)
            # 2. Auto-Fetch Logic
            # Default empty values
            val_name = ""
            val_cat = "Antibiotic"
            val_price = 0.01
            val_stock = 0
            val_exp = date.today()
            val_sup_index = 0
            exists = False
            # Fetch suppliers first to handle dropdown index
            sup_df = pd.read_sql("SELECT SupplierID, CompanyName FROM Suppliers", conn)
            sup_list = sup_df['CompanyName'].tolist() if not sup_df.empty else []
            # Check if Medicine exists
            curr_med = pd.read_sql(f"SELECT * FROM Medicines WHERE MedicineID={m_id}", conn)
            if not curr_med.empty:
                exists = True
                st.success(f"🔹 Found: **{curr_med.iloc[0]['Medicine_Name']}** (Data Loaded)")
                # Fill variables from DB
                row = curr_med.iloc[0]
                val_name = row['Medicine_Name']
                val_cat = row['Category']
                val_price = float(row['Price'])
                val_stock = int(row['StockQuantity'])
                try:
                    val_exp = pd.to_datetime(row['ExpiryDate']).date()
                except:
                    pass
                # Match Supplier
                saved_sup_id = row['SupplierID']
                if not sup_df.empty:
                    found_sup = sup_df[sup_df['SupplierID'] == saved_sup_id]
                    if not found_sup.empty:
                        sup_name_str = found_sup.iloc[0]['CompanyName']
                        if sup_name_str in sup_list:
                            val_sup_index = sup_list.index(sup_name_str)
            else:
                st.info("✨ New Item (Ready to Add)")
            # 3. Inputs with 'value=' parameter
            c1, c2, c3 = st.columns(3)
            m_name = c1.text_input("Medicine_Name", value=val_name)
            # Handle category index safely
            cat_options = ["Antibiotic", "Painkiller", "Chronic", "Vitamins", "Other"]
            cat_index = cat_options.index(val_cat) if val_cat in cat_options else 0
            m_cat = c2.selectbox("Category", cat_options, index=cat_index)
            sup_name = c3.selectbox("Supplier", sup_list, index=val_sup_index) if sup_list else None
            c4, c5, c6 = st.columns(3)
            m_price = c4.number_input("Price (EGP)", min_value=0.01, value=val_price)
            m_stock = c5.number_input("Stock Qty", min_value=0, value=val_stock)
            m_exp = c6.date_input("Expiry Date", value=val_exp)

            # 4. Action Buttons
            b1, b2, b3 = st.columns(3)
            if b1.button("➕ Add New", use_container_width=True, disabled=exists):
                try:
                    sup_id = int(sup_df[sup_df['CompanyName'] == sup_name]['SupplierID'].iloc[0])

                    conn.cursor().execute("INSERT INTO Medicines VALUES (?,?,?,?,?,?,?)",
                                          (m_id, m_name, m_cat, m_price, m_stock, str(m_exp), sup_id)).commit()
                    st.success("Added successfully!");
                    st.rerun()
                except Exception as e:
                    st.error(e)
            if b2.button("🔄 Update", use_container_width=True, disabled=not exists):
                try:
                    conn.cursor().execute(
                        "UPDATE Medicines SET Medicine_Name=?, Category=?, Price=?, StockQuantity=?, ExpiryDate=? WHERE MedicineID=?",
                        (m_name, m_cat, m_price, m_stock, str(m_exp), m_id)).commit()
                    st.success("Updated successfully!");
                    st.rerun()
                except Exception as e:
                    st.error(e)
            if b3.button("🗑️ Archive (Remove)", type="primary", use_container_width=True, disabled=not exists):
                try:
                    # Soft Delete Strategy:
                    # 1. We set StockQuantity to 0 (so it disappears from POS).
                    # 2. We change the name to indicate it's archived.
                    # 3. We DO NOT actually delete the row, so history remains safe.

                    new_name = f"{m_name} (Archived)"

                    conn.cursor().execute(
                        "UPDATE Medicines SET StockQuantity = 0, Medicine_Name = ? WHERE MedicineID = ?",
                        (new_name, m_id)
                    ).commit()

                    st.success("Item archived successfully! It is now hidden from the sales screen.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        st.divider()
        st.dataframe(pd.read_sql("SELECT * FROM Medicines", conn), use_container_width=True)
        conn.close()

# --- CUSTOMERS ---
elif page == "Customers":
    st.title("👥 Customers Management")
    conn = get_connection()
    if conn:
        with st.container(border=True):
            cid = st.number_input("Customer ID", 1)
            # Defaults
            v_name, v_phone, v_age = "", "", 1
            exists = False
            # Auto-Fetch
            curr = pd.read_sql(f"SELECT * FROM Customers WHERE CustomerID={cid}", conn)
            if not curr.empty:
                exists = True
                st.success(f"🔹 Loaded: {curr.iloc[0]['FullName']}")
                v_name = curr.iloc[0]['FullName']
                v_phone = curr.iloc[0]['Phone']
                v_age = int(curr.iloc[0]['Age'])
            else:
                st.info("✨ New Customer ID")
            c1, c2, c3 = st.columns(3)
            cname = c1.text_input("Full Name", value=v_name)
            cph = c2.text_input("Phone", value=v_phone)
            cage = c3.number_input("Age", 1, value=v_age)

            b1, b2, b3 = st.columns(3)
            if b1.button("➕ Add", disabled=exists, use_container_width=True):
                conn.cursor().execute("INSERT INTO Customers VALUES (?,?,?,?)", (cid, cname, cph, cage)).commit();
                st.rerun()
            if b2.button("🔄 Update", disabled=not exists, use_container_width=True):
                conn.cursor().execute("UPDATE Customers SET FullName=?, Phone=?, Age=? WHERE CustomerID=?",
                                      (cname, cph, cage, cid)).commit();
                st.rerun()
            if b3.button("🗑️ Delete", type="primary", disabled=not exists, use_container_width=True):
                conn.cursor().execute("DELETE FROM Customers WHERE CustomerID=?", (cid,)).commit();
                st.rerun()
        st.dataframe(pd.read_sql("SELECT * FROM Customers", conn), use_container_width=True)
        conn.close()

# --- DOCTORS ---
elif page == "Doctors":
    st.title("👨‍⚕️ Doctors Registry")
    conn = get_connection()
    if conn:
        with st.container(border=True):
            did = st.number_input("Doctor ID", 1)
            v_name, v_spec, v_phone = "", "", ""
            exists = False

            curr = pd.read_sql(f"SELECT * FROM Doctors WHERE DoctorID={did}", conn)
            if not curr.empty:
                exists = True
                st.success(f"🔹 Loaded: {curr.iloc[0]['Doctor_Name']}")
                v_name = curr.iloc[0]['Doctor_Name']
                v_spec = curr.iloc[0]['Specialty']
                v_phone = curr.iloc[0]['Phone']
            else:
                st.info("✨ New Doctor ID")
            c1, c2, c3 = st.columns(3)
            dname = c1.text_input("Name", value=v_name)
            dspec = c2.text_input("Specialty", value=v_spec)
            dphone = c3.text_input("Phone", value=v_phone)
            b1, b2, b3 = st.columns(3)
            if b1.button("➕ Add", disabled=exists, use_container_width=True):
                conn.cursor().execute("INSERT INTO Doctors VALUES (?,?,?,?)", (did, dname, dspec, dphone)).commit();
                st.rerun()
            if b2.button("🔄 Update", disabled=not exists, use_container_width=True):
                conn.cursor().execute("UPDATE Doctors SET Doctor_Name=?, Specialty=?, Phone=? WHERE DoctorID=?",
                                      (dname, dspec, dphone, did)).commit();
                st.rerun()
            if b3.button("🗑️ Delete", type="primary", disabled=not exists, use_container_width=True):
                conn.cursor().execute("DELETE FROM Doctors WHERE DoctorID=?", (did,)).commit();
                st.rerun()
        st.dataframe(pd.read_sql("SELECT * FROM Doctors", conn), use_container_width=True)
        conn.close()

# --- SUPPLIERS ---
elif page == "Suppliers":
    st.title("🚛 Suppliers Management")
    conn = get_connection()
    if conn:
        with st.container(border=True):
            sid = st.number_input("Supplier ID", 1)
            v_comp, v_cont, v_ph, v_adr = "", "", "", ""
            exists = False
            curr = pd.read_sql(f"SELECT * FROM Suppliers WHERE SupplierID={sid}", conn)
            if not curr.empty:
                exists = True
                row = curr.iloc[0]
                st.success(f"🔹 Loaded: **{row['CompanyName']}**")
                v_comp = row['CompanyName']
                v_cont = row['ContactName']
                v_ph = row['Phone']
                v_adr = row['Address']
            else:
                st.info("✨ New Supplier ID")
            sname = st.text_input("Company Name", value=v_comp)
            c1, c2, c3 = st.columns(3)
            scont = c1.text_input("Contact Person", value=v_cont)
            sph = c2.text_input("Phone", value=v_ph)
            sadr = c3.text_input("Address", value=v_adr)
            b1, b2, b3 = st.columns(3)
            if b1.button("➕ Add", disabled=exists, use_container_width=True):
                conn.cursor().execute("INSERT INTO Suppliers VALUES (?,?,?,?,?)",
                                      (sid, sname, scont, sph, sadr)).commit();
                st.rerun()
            if b2.button("🔄 Update", disabled=not exists, use_container_width=True):
                conn.cursor().execute(
                    "UPDATE Suppliers SET CompanyName=?, ContactName=?, Phone=?, Address=? WHERE SupplierID=?",
                    (sname, scont, sph, sadr, sid)).commit();
                st.rerun()
            if b3.button("🗑️ Delete", type="primary", disabled=not exists, use_container_width=True):
                conn.cursor().execute("DELETE FROM Suppliers WHERE SupplierID=?", (sid,)).commit();
                st.rerun()
        st.dataframe(pd.read_sql("SELECT * FROM Suppliers", conn), use_container_width=True)
        conn.close()

# --- PRESCRIPTIONS ---
elif page == "Prescriptions":
    st.title("📑 Prescriptions")
    conn = get_connection()
    if conn:
        custs = pd.read_sql("SELECT CustomerID, FullName FROM Customers", conn)
        docs = pd.read_sql("SELECT DoctorID, Doctor_Name FROM Doctors", conn)
        if custs.empty or docs.empty:
            st.warning("⚠️ Add Doctors/Customers first.")
        else:
            with st.container(border=True):
                c1, c2 = st.columns(2)
                pid = c1.number_input("Prescription ID", 1)
                # Auto-Fill
                v_date = date.today()
                v_note = ""
                ix_cust = 0
                ix_doc = 0
                exists = False
                curr = pd.read_sql(f"SELECT * FROM Prescriptions WHERE PrescriptionID={pid}", conn)
                if not curr.empty:
                    exists = True
                    st.success(f"🔹 Loaded Prescription #{pid}")
                    try:
                        v_date = pd.to_datetime(curr.iloc[0]['IssueDate']).date()
                    except:
                        pass
                    v_note = curr.iloc[0]['Notes']
                    saved_cid = curr.iloc[0]['CustomerID']
                    saved_did = curr.iloc[0]['DoctorID']
                    c_list = custs['CustomerID'].tolist()
                    if saved_cid in c_list: ix_cust = c_list.index(saved_cid)

                    d_list = docs['DoctorID'].tolist()
                    if saved_did in d_list: ix_doc = d_list.index(saved_did)
                else:
                    st.info("✨ New Prescription")
                pdate = c2.date_input("Date", value=v_date)
                c3, c4 = st.columns(2)
                sel_c = c3.selectbox("Patient", custs['FullName'], index=ix_cust)
                sel_d = c4.selectbox("Doctor", docs['Doctor_Name'], index=ix_doc)
                note = st.text_area("Diagnosis / Medications", value=v_note)
                b1, b2, b3 = st.columns(3)
                if b1.button("💾 Save New", disabled=exists, use_container_width=True, key="btn_save_presc"):
                    try:
                        cid = int(custs[custs['FullName'] == sel_c]['CustomerID'].iloc[0])
                        did = int(docs[docs['Doctor_Name'] == sel_d]['DoctorID'].iloc[0])
                        conn.cursor().execute("INSERT INTO Prescriptions VALUES (?,?,?,?,?)",
                                              (int(pid), str(pdate), note, cid, did)).commit();
                        st.success("Saved successfully!")
                        st.rerun()
                    except pyodbc.IntegrityError:
                        st.error(f"❌ Error: Prescription ID ({pid}) already exists. Please choose a different ID.")
                    except Exception as e:
                        st.error(f"Error: {e}")
                if b2.button("🔄 Update Existing", disabled=not exists, use_container_width=True,
                             key="btn_update_presc"):
                    cid = int(custs[custs['FullName'] == sel_c]['CustomerID'].iloc[0])
                    did = int(docs[docs['Doctor_Name'] == sel_d]['DoctorID'].iloc[0])
                    conn.cursor().execute(
                        "UPDATE Prescriptions SET IssueDate=?, Notes=?, CustomerID=?, DoctorID=? WHERE PrescriptionID=?",
                        (str(pdate), note, cid, did, int(pid))).commit();
                    st.success("Updated successfully!")
                if b3.button("🗑️ Delete", type="primary", disabled=not exists, use_container_width=True,
                             key="btn_delete_presc"):
                    conn.cursor().execute("DELETE FROM Prescriptions WHERE PrescriptionID=?", (int(pid),)).commit();
                    st.warning("Deleted successfully!")


        st.divider()
        st.subheader("History")
        st.dataframe(pd.read_sql("SELECT P.PrescriptionID, P.IssueDate, C.FullName, D.Doctor_Name, P.Notes FROM Prescriptions P JOIN Customers C ON P.CustomerID=C.CustomerID JOIN Doctors D ON P.DoctorID=D.DoctorID",
                                 conn),
                     use_container_width=True)
        conn.close()