# This file is mainly used to manage the critical data in the database.
# It is used to add, remove, and update servers.
# It is used to add, remove, and update keys.

# IT SHOULD NEVER BE USED TO RUN DIRECTLY.


import sqlite3
from .dbinitalization import init_db

def initdb():
    # This should only be used on the first run.
    init_db()

def add_server(ip, port, username, password, keyid):
    # THIS IS THE REDUNDANT FUNCTION.
    # THIS IS REPLACED BY .operate.addserverviapwd and .operate.addserverviakey
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("INSERT INTO servers (ip, port, username, password, keyid) VALUES (?, ?, ?, ?, ?)", (ip, port, username, password, keyid))
    conn.commit()
    conn.close()
    print("Server added.")

def remove_server(ip, port, username, password, keyid):
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("DELETE FROM servers WHERE ip=?", (ip))
    conn.commit()
    conn.close()
    print("Server removed.")
    
def update_server(ip, port, username, password, keyid):
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("UPDATE servers SET ip=?, port=?, username=?, password=?, keyid=? WHERE ip=?", (ip, port, username, password, keyid, ip))
    conn.commit()
    conn.close()
    print("Server updated.")

def list_servers():
    # This function is newly added to return all the server IPs and usernames.
    # To let users choose their servers conveniently instead of having to remember all those tedious IPs.
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("SELECT ip, username FROM servers")
    servers = c.fetchall()
    conn.close()
    return servers

def add_key(keyfile):
    # The private key is usually in a file so we need to read it in.
    with open(keyfile, 'r') as f:
        key = f.read()
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("INSERT INTO keys (key) VALUES (?)", (key))
    # Read the ID
    keyid = c.lastrowid
    conn.commit()
    conn.close()
    print("Key added with key ID: " + str(keyid))
    return keyid # The keyid is already integer... Well we will see.

def remove_key(keyid):
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("DELETE FROM keys WHERE id=?", (keyid))
    conn.commit()
    conn.close()
    print("Key removed.")

def list_keys():
    # This function is newly added to return all the key IDs and descriptions.
    # To let users choose their keys conveniently instead of having to remember all those tedious IDs.
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("SELECT id, description FROM keys")
    keys = c.fetchall()
    conn.close()
    return keys

# Copyright (C) 2022 Frank Ruan w/ GitHub Copilot.
# Licensed under GPLv3.0.