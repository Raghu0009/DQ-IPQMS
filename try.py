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


def get_executable_directory():
    import sys
    if getattr(sys, 'frozen', False):  # check if running as a bundled executable
        return os.path.dirname(sys.executable)  # return directory of the executable
    else:
        return os.path.dirname(os.path.abspath(__file__))  # return directory of the script



def print_data(connection, schd):
    query = "SELECT * FROM ol_unit_schd_dtl WHERE ID_SCHD = :schd"
    df = pd.read_sql_query(query, connection, params={'schd': schd})
    if not df.empty:
        print(df)
    else:
        print("No data found for the given ID_SCHD:", schd)

try:
    conn = cx_Oracle.connect(username, password, dsn)
    print("Connected to Oracle Database.")
    schd = 17765
    print_data(conn, schd)

except cx_Oracle.Error as error:
    print("Error connecting to Oracle database:", error)

finally:
    if conn:
        conn.close()
        print("Connection closed.")
