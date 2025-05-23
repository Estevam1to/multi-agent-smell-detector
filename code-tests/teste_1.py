import sqlite3

class UserManager:
    def __init__(self, db_path, smtp_server, smtp_port, email_user, email_pass, log_file, cache_enabled):
        self.db_path = db_path
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_user = email_user
        self.email_pass = email_pass
        self.log_file = log_file
        self.cache_enabled = cache_enabled
        self.cache = {}

    def process_request(self, action, user_id, user_name=None, email=None, age=None, country=None):
        # Long Method + Too Many Branches
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = f"SELECT * FROM users WHERE id = {user_id}"
        cursor.execute(query)
        user = cursor.fetchone()

        if not user:
            with open(self.log_file, 'a') as log:
                log.write(f"User {user_id} not found\n")
            return False

        if action == 'update':
            success = self.update_user(user_id, user_name, email, age, country, True, 'system')
            if success:
                self.send_email(email, "Profile updated", f"Hello {user_name}, your profile was updated.")
                return True
            else:
                return False

        elif action == 'delete':
            cursor.execute(f"DELETE FROM users WHERE id = {user_id}")
            conn.commit()
            self.send_email(user[2], "Account deleted", f"Goodbye {user[1]}")
            return True

        else:
            return False

    def update_user(self, uid, name, email, age, country, notify, actor):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        sql = "UPDATE users SET name = '%s', email = '%s', age = %s, country = '%s' WHERE id = %s" % (
            name, email, age, country, uid
        )
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            with open(self.log_file, 'a') as log:
                log.write(f"Error updating user {uid}: {e}\n")
            return False

        if notify:
            self.send_email(email, "Update notice", f"Your profile was updated by {actor}")
        return True

    def send_email(self, to_address, subject, body):
        print(f"Conectando ao {self.smtp_server}:{self.smtp_port} como {self.email_user}")
        print(f"Enviando email para {to_address}: {subject}\n{body}")
