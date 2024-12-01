import json

def create_workspace(conn, name, apps):
    cursor = conn.cursor()
    apps_json = json.dumps(apps)
    cursor.execute("INSERT INTO workspaces (name, apps) VALUES (?, ?)", (name, apps_json))
    conn.commit()

def get_workspaces(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name, apps FROM workspaces")
    workspaces = cursor.fetchall()
    return [{"name": row[0], "apps": json.loads(row[1])} for row in workspaces]

def launch_workspace(conn, name):
    cursor = conn.cursor()
    cursor.execute("SELECT apps FROM workspaces WHERE name = ?", (name,))
    row = cursor.fetchone()
    if row:
        apps = json.loads(row[0])
        for app in apps:
            os.system(f"open -a {app}")
        return True
    return False
