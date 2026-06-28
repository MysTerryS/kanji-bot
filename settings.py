from database import conn

def set_default(user_id):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO user_settings (user_id)
        VALUES (?)
    """, (user_id, ))
    conn.commit()

def get_user_settings(user_id):
    cursor = conn.cursor()
    set_default(user_id)
    cursor.execute("""
        SELECT * FROM user_settings
        WHERE user_id = ?
    """, (user_id,))
    row = cursor.fetchone()
    return dict(zip(
        [col[0] for col in cursor.description],
        row
    ))

def update_radical_level(user_id, level):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE user_settings
        SET radical_level = ?
        WHERE user_id = ?
    """, (level, user_id))
    conn.commit()

def ShowSettings(user_id):
    settings = get_user_settings(user_id)
    answer = "Your current settings:\n"
    for key, value in settings.items():
        answer += "{}: {}\n".format(key, value)
    return answer