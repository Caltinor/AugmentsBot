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
    sql = 'SELECT message_body, mod_version, embed_image FROM info WHERE cmdroot = ? AND keyword = ? AND mod_version LIKE ?;'
    return cursor.execute(sql, (modID, keyword, f'%{filter}%')).fetchall()

def get_info_formatted(modID :str, keyword :str, filter :str):
    results = get_info(modID, keyword, filter)
    formatted_lines = []
    for result in results:
        embed = discord.Embed(title=f"{keyword} for {modID} version {result[1]}:", description=result[0], color=discord.Color.blue())
        if result[2] == None or len(result[2]) > 0:
            embed.set_image(url=result[2])
        formatted_lines.append(embed)
    return formatted_lines if len(formatted_lines) > 0 else [discord.Embed(title='This keyword has no associated documentation')]

def set_info(modID :str, keyword :str, version :str, message :str, img :str):
    insert_sql = 'INSERT INTO info (cmdroot, keyword, mod_version, message_body, embed_image) VALUES(?,?,?,?,?);'
    update_sql = 'UPDATE info SET message_body = ?, embed_image = ? WHERE cmdroot = ? AND keyword = ? AND mod_version = ?;'
    results = get_info(modID=modID, keyword=keyword, filter=version)
    if len(results) > 0:
        connection.execute(update_sql, (message, img, modID, keyword, version))
    else:
        connection.execute(insert_sql, (modID, keyword, version, message, img)) 
    connection.commit()

def get_compat(mod_a :str, mod_b :str, filter :str):
    sql = 'SELECT message_body, mod_a_version, embed_image FROM compat WHERE mod_a = ? AND mod_b = ? AND mod_a_version LIKE ?;'
    return cursor.execute(sql, (mod_a, mod_b, f'%{filter}%')).fetchall()    

def get_compat_formatted(mod_a :str, mod_b :str, filter :str):
    results = get_compat(mod_a=mod_a, mod_b=mod_b, filter=filter)
    formatted_lines = []
    for result in results:
        embed = discord.Embed(title=f"{mod_a} compat with {mod_b} for version {result[1]}:", description=result[0], color=discord.Color.yellow())
        if result[2] == None or len(result[2]) > 0:
            embed.set_image(url=result[2])
        formatted_lines.append(embed)
    return formatted_lines if len(formatted_lines) > 0 else [discord.Embed(title='No incompatibilities have been reported for these mods and version.')]

def set_compat(mod_a :str, mod_b :str, version :str, message :str, img :str):
    insert_sql = 'INSERT INTO compat (mod_a, mod_b, message_body, mod_a_version, embed_image) VALUES("?,?,?,?,?);'
    update_sql = 'UPDATE compat SET message_body = ?, embed_image = ? WHERE mod_a = ? AND mod_b = ? AND mod_a_version = ?;'
    results = get_compat(mod_a=mod_a, mod_b=mod_b, filter=version)
    if len(results) > 0:
        connection.execute(update_sql, (message, img, mod_a, mod_b, version))
    else:
        connection.execute(insert_sql, (mod_a, mod_b, message, version, img))
    connection.commit()

def list_info(modID :str, filter :str):
    sql = 'SELECT keyword, mod_version FROM info WHERE cmdroot = ? AND mod_version LIKE ?;'
    keywordList = cursor.execute(sql, (modID, f'%{filter}%')).fetchall()
    items = []
    for item in keywordList:
        items.append(f'`{item[0]}`({item[1]})')
    items.sort()
    return "\n".join(items) if len(items) > 0 else "No Keywords."

def list_compat(mod_a :str, filter :str):
    sql = f'SELECT mod_b, mod_a_version FROM compat WHERE mod_a = ? AND mod_a_version LIKE ?;'
    keywordList = cursor.execute(sql, (mod_a, f'%{filter}%')).fetchall()
    items = []
    for item in keywordList:
        items.append(f'`{item[0]}`({item[1]})')
    items.sort()
    return "\n".join(items) if len(items) > 0 else "No Keywords."