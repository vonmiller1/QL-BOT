from sqlalchemy import create_engine, text

db_engine = create_engine("sqlite:///employee_db.sqlite")

with db_engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS employees"))
    conn.execute(text("""
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY, 
            name TEXT UNIQUE, 
            designation TEXT, 
            department TEXT, 
            salary REAL
        )
    """))
    
    conn.execute(text("INSERT INTO employees (name, designation, department, salary) VALUES ('hrithik', 'AI Engineer', 'AI', 120000)"))
    conn.commit()