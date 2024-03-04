import os
import sqlite3


# Directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


# Database Path
DB_PATH = os.path.join(SCRIPT_DIR, '..', 'db', 'db.sqlite3')


# Database Connection
def get_connection():
    return sqlite3.connect(DB_PATH)


# Create tasks Table
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS tasks (
            TaskId INTEGER PRIMARY KEY AUTOINCREMENT,
            TaskName TEXT ,
            TaskDescription TEXT,
            TaskDate TEXT,
            TaskTime TEXT
        );
        """

        cursor.execute(create_table_query)
        conn.commit()

        return {
            'success': 'true',
            'message': 'Table created successfully'
        }
    except Exception as e:
        return {
            'success': 'false',
            'message': f'Error: {str(e)}'
        }
    finally:
        cursor.close()
        conn.close()
# ------------------------------------------------------------------------------------


# Add Task
def add_task(data):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Execute the SQL query to insert the task into the table
        insert_query = """
        INSERT INTO tasks (TaskName, TaskDescription, TaskDate, TaskTime)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(
            insert_query, (data['taskName'], data['taskDescription'], data['taskDate'], data['taskTime']))
        conn.commit()

        return {
            'success': 'true',
            'message': 'Task added successfully'
        }
    except Exception as e:
        return {
            'success': 'false',
            'message': f'Error: {str(e)}'
        }
    finally:
        cursor.close()
        conn.close()
# ------------------------------------------------------------------------------------


# Edit Task
def edit_task(data):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Execute the SQL query to update the task in the table
        update_query = """
        UPDATE tasks
        SET TaskName = ?,
            TaskDescription = ?,
            TaskDate = ?,
            TaskTime = ?
        WHERE TaskId = ?
        """
        cursor.execute(update_query, (data['taskName'], data['taskDescription'],
                       data['taskDate'], data['taskTime'], data['taskId']))
        conn.commit()

        return {
            'success': 'true',
            'message': 'Task edited successfully'
        }
    except Exception as e:
        return {
            'success': 'false',
            'message': f'Error: {str(e)}'
        }
    finally:
        cursor.close()
        conn.close()
# ------------------------------------------------------------------------------------


# Delete Task
def delete_task(data):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Execute the SQL query to delete the task from the table
        delete_query = """
        DELETE FROM tasks
        WHERE TaskId = ?
        """

        cursor.execute(delete_query, (int(data['taskId']),))
        conn.commit()

        return {
            'success': 'true',
            'message': 'Task deleted successfully'
        }
    except Exception as e:
        return {
            'success': 'false',
            'message': f'Error: {str(e)}'
        }
    finally:
        cursor.close()
        conn.close()
# ------------------------------------------------------------------------------------


# Get All Tasks
def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Execute the SQL query to get all tasks from the table
        select_query = """
        SELECT * FROM tasks
        """
        cursor.execute(select_query)

        # Fetch all rows
        tasks = cursor.fetchall()

        if not tasks:
            return {
                'success': 'false',
                'message': 'No Tasks Found!'
            }

        return {
            'success': 'true',
            'message': 'Tasks retrieved successfully',
            'tasks': tasks
        }
    except Exception as e:
        return {
            'success': 'false',
            'message': f'Error: {str(e)}'
        }
    finally:
        cursor.close()
        conn.close()
# ------------------------------------------------------------------------------------


if __name__ == "__main__":
    print(create_table())
