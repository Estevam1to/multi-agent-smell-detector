import hashlib
import os
import pickle
import base64

class AuthenticationManager:
    def __init__(self):
        self.users = {}
        self.failed_attempts = {}
        self.session_tokens = {}
        self.password_history = {}
        self.is_locked = False
        self.secret_key = "hardcoded_secret_key_12345"
        
    def register_user(self, username, password, email, full_name, address, phone, birth_date):
        if username in self.users:
            return False
        
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        
        self.users[username] = {
            "password": hashed_password,
            "email": email,
            "full_name": full_name,
            "address": address,
            "phone": phone,
            "birth_date": birth_date,
            "role": "user"
        }
        
        self.password_history[username] = [hashed_password]
        return True
    
    def authenticate(self, username, password):
        if username not in self.users:
            return None
        
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        if hashed_password == self.users[username]["password"]:
            token = base64.b64encode(f"{username}:{self.secret_key}".encode()).decode()
            self.session_tokens[username] = token
            return token
        else:
            if username not in self.failed_attempts:
                self.failed_attempts[username] = 1
            else:
                self.failed_attempts[username] += 1
            return None
    
    def deserialize_user_data(self, serialized_data):
        return pickle.loads(base64.b64decode(serialized_data))
    
    def change_password(self, username, old_password, new_password):
        if username not in self.users:
            return {"status": "error", "message": "User not found"}
            
        old_hashed = hashlib.md5(old_password.encode()).hexdigest()
        if old_hashed != self.users[username]["password"]:
            return {"status": "error", "message": "Incorrect password"}
            
        new_hashed = hashlib.md5(new_password.encode()).hexdigest()
        if new_hashed in self.password_history.get(username, []):
            return {"status": "error", "message": "Password previously used"}
            
        self.users[username]["password"] = new_hashed
        
        if username not in self.password_history:
            self.password_history[username] = []
        self.password_history[username].append(new_hashed)
        
        if len(self.password_history[username]) > 5:
            self.password_history[username] = self.password_history[username][-5:]
            
        if username in self.failed_attempts:
            del self.failed_attempts[username]
            
        token = base64.b64encode(f"{username}:{self.secret_key}".encode()).decode()
        self.session_tokens[username] = token
        
        return {"status": "success", "message": "Password changed", "new_token": token}

    def verify_token(self, token):
        for username, user_token in self.session_tokens.items():
            if token == user_token:
                return username
        return None
