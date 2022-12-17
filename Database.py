import discord
import sqlite3
import discord.ui

connection = sqlite3.connect('bot_data.db')
cursor = connection.cursor()
print("Database Connection Established")

#execute table definitions
cursor.executescript(open('table_definitions.sql', 'r').read())
print("Tables constructed if absent")

def get_info(modID :str, keyword :str, filter :str):
    sql = f'SELECT message_body, mod_version FROM info WHERE cmdroot = "{modID}" AND keyword = "{keyword}" AND mod_version LIKE "%{filter}%";'
    return cursor.execute(sql).fetchall()

def get_info_formatted(modID :str, keyword :str, filter :str):
    results = get_info(modID, keyword, filter)
    formatted_lines = []
    for result in results:

        embed = discord.Embed(title=f"{keyword} for {modID} version {result[1]}:", description=result[0], color=discord.Color.blue())
        formatted_lines.append(embed)
    return formatted_lines if len(formatted_lines) > 0 else [discord.Embed(title='This keyword has no associated documentation')]

def set_info(modID :str, keyword :str, version :str, message :str):
    insert_sql = f'INSERT INTO info (cmdroot, keyword, mod_version, message_body) VALUES("{modID}","{keyword}","{version}","{message}");'
    update_sql = f'UPDATE info SET message_body = "{message}" WHERE cmdroot = "{modID}" AND keyword = "{keyword}" AND mod_version = "{version}";'
    results = get_info(modID=modID, keyword=keyword, filter=version)
    final_sql = update_sql if len(results) > 0 else insert_sql
    connection.execute(final_sql)
    connection.commit()

def get_compat(mod_a :str, mod_b :str, filter :str):
    sql = f'SELECT message_body, mod_a_version FROM compat WHERE mod_a = "{mod_a}" AND mod_b = "{mod_b}" AND mod_a_version LIKE "%{filter}%";'
    return cursor.execute(sql).fetchall()    

def get_compat_formatted(mod_a :str, mod_b :str, filter :str):
    results = get_compat(mod_a=mod_a, mod_b=mod_b, filter=filter)
    formatted_lines = []
    for result in results:
        embed = discord.Embed(title=f"{mod_a} compat with {mod_b} for version {result[1]}:", description=result[0], color=discord.Color.yellow())
        formatted_lines.append(embed)
    return formatted_lines if len(formatted_lines) > 0 else [discord.Embed(title='No incompatibilities have been reported for these mods and version.')]

def set_compat(mod_a :str, mod_b :str, version :str, message :str):
    insert_sql = f'INSERT INTO compat (mod_a, mod_b, message_body, mod_a_version) VALUES("{mod_a}","{mod_b}","{message}","{version}");'
    update_sql = f'UPDATE compat SET message_body = "{message}" WHERE mod_a = "{mod_a}" AND mod_b = "{mod_b}" AND mod_a_version = "{version}";'
    results = get_compat(mod_a=mod_a, mod_b=mod_b, filter=version)
    final_sql = update_sql if len(results) > 0 else insert_sql
    connection.execute(final_sql)
    connection.commit()