from dotenv import load_dotenv
load_dotenv()

import frappe

import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@frappe.whitelist()
def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

def read_sql_query(sql,db):
    return None

prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database consists of multiple tables used in the Frappe and ERPNext system. The table names are in the format 'tab[Table Name]', for example, 'tabStudent', 'tabEmployee', 'tabSales Order', etc. Each table has several columns corresponding to different attributes.

    Some example questions and their SQL queries are given below:

    Example 1 - How many records are present in the Student table?, 
    the SQL command will be something like this: 
    SELECT COUNT(*) FROM `tabStudent`;

    Example 2 - List all employees in the HR department?, 
    the SQL command will be something like this: 
    SELECT * FROM `tabEmployee` WHERE department='HR';

    Example 3 - Show all sales orders created in the year 2023?, 
    the SQL command will be something like this: 
    SELECT * FROM `tabSales Order` WHERE YEAR(transaction_date) = 2023;

    The SQL commands should be precise and NOT include any unnecessary keywords or formatting like ``` or "sql" blocks. The output should only contain plain SQL code without any special symbols.

    The SQL commands should be precise and not include any unnecessary keywords or formatting characters like ``` in the output.
    If the column names contain spaces, replace them with underscores (_) in the SQL query.
    The SQL queries should be based on user input, accurately translating the question to SQL commands.

     Common terms used by users and their mappings:
    - "bills" refers to the `tabPurchase Invoice` table.
    - "employees" refers to the `tabEmployee` table.
    - "orders" refers to the `tabSales Order` or `tabPurchase Order` table, depending on the context.
    - "students" refers to the `tabStudent` table.
    - "projects" refers to the `tabProject` table.

    Tables used in Frappe/ERPNext:
    - `tabStudent` (NAME, CLASS, SECTION, GRADE, etc.)
    - `tabEmployee` (EMPLOYEE_NAME, DEPARTMENT, DESIGNATION, etc.) -- Use the "status" column to indicate employee status (e.g., Active, Left).
    - `tabSales Order` (ORDER_ID, CUSTOMER_NAME, TRANSACTION_DATE, etc.)
    - `tabPurchase Order` (SUPPLIER, ORDER_DATE, STATUS, etc.)
    - `tabInvoice` (INVOICE_NO, CUSTOMER, AMOUNT, etc.)
    - `tabProject` (PROJECT_NAME, START_DATE, END_DATE, etc.)
    - `tabPurchase Invoice` (INVOICE_NO, STATUS, AMOUNT, etc.) -- Use the "status" column for payment or completion status.

    Please generate the SQL query based on the user's input and ensure no code block formatting or ``` characters are present in the response.
    """
]