from database import Database

activities={
    "login": "Logged In",
    "add_fee": "Added fee data for {} sem {}",
    "edit_fee": "Edited fee data for {} sem {}",
    "delete_fee": "Deleted fee data for {} sem {}",
    "print_fee": "Printed fee data for reg. no. {}",
    "send_notification": "Send notification via email",
    "print_batch_fee":  "Printed batch fee detail",
    "logout": "Logged Out"
}

def create_log(dnt, uname, activity):
    db= Database()
    conn= db.connect_database("user_log.db")
    with open("logs.sql", "r") as table:
        db.create_table(table.read(),conn)
    
    data= (dnt,  uname, activity)
    db.insert_into_database("user_logs",conn,data)

def extract_log():
    db= Database()
    conn= db.connect_database("user_log.db")
    try:
        data= db.extractAllData("user_log.db","user_logs",order_by="id")[::-1]
        return data
    except TypeError:
        return None

