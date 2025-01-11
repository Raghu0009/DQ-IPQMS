import pandas as pd
import cx_Oracle
import os

username = 'SPT001A'
password = 'WELCOME'
host = '10.10.1.166'
port = 1522
service = 'SPTSUAT'
dsn = cx_Oracle.makedsn(host, port, service)

cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient-basic-windows.x64-11.2.0.4.0\instantclient_11_2")


try:
    conn = cx_Oracle.connect(username, password, dsn)
    print("Connected to Oracle Database.")

    schd = 17765
    query = "SELECT * FROM ol_unit_schd_dtl WHERE ID_SCHD = :schd"
    df = pd.read_sql(query, conn, params={'schd': schd})

    if not df.empty:
        output_folder = os.path.join(os.getcwd(), "Excel_Outputs")
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, f"ol_unit_schd_dtl_{schd}.xlsx")
        df.to_excel(output_path, index=False)
        print(f"Data saved to: {output_path}")
    else:
        print(f"No data found for ID_SCHD: {schd}")

except cx_Oracle.Error as e:
    print(f"Error: {e}")

finally:
    if conn:
        conn.close()
        print("Connection closed.")
