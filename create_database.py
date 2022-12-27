import sqlite3

conn = sqlite3.connect('chtrli.db')

print("Opened database succwessfully")

cur = conn.cursor()

cur.execute("""CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT,
        uname TEXT NOT NULL UNIQUE,
        pswd TEXT NOT NULL,
        admin SMALLINT DEFAULT 0)""")

cur.execute("""INSERT INTO users ( uname, pswd, admin) VALUES ('admin', 'admin', '1')""")
cur.execute("""INSERT INTO users ( uname, pswd) VALUES ('user', 'user')""")
cur.execute("""INSERT INTO users (id, uname, pswd, admin) VALUES ('0','guest', 'guest', '0')""")

cur.execute("""CREATE TABLE likes_songs (uid INTEGER,
        song_id INTEGER NOT NULL)""")

cur.execute("""CREATE TABLE likes_sugg (uid INTEGER,
        sugg_id INTEGER NOT NULL)""")

cur.execute("""CREATE TABLE suggestions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid SMALLINT NOT NULL,
        song_name TEXT NOT NULL,
        name_std TEXT NOT NULL,
        song_author TEXT NOT NULL,
        likes INTEGER DEFAULT 0)""")

cur.execute("""INSERT INTO suggestions (uid, song_name,name_std, song_author)
        VALUES ('2','Pulnocni','pulnocni', 'Karel Cech')""")
cur.execute("""INSERT INTO suggestions (uid, song_name,name_std, song_author)
        VALUES ('1','Lighthouse keeper','ligthouse keeper', 'Sam Smith')""")
cur.execute("""INSERT INTO suggestions (uid, song_name, name_std,song_author)
        VALUES ('2','Last Christmas', 'last christmas','WHAM')""")

cur.execute("""INSERT INTO suggestions (uid, song_name, name_std, song_author)
        VALUES ('1','Daj Boh stastia tejto zemi', 'daj boh stastia tejto zemi','Zbor')""")

cur.execute("""INSERT INTO suggestions (uid, song_name,name_std, song_author)
        VALUES ('2','Thank God it''s Christmas', 'thank god its christmas','The Queen')""")

cur.execute("""INSERT INTO suggestions (uid, song_name, name_std, song_author)
        VALUES ('1','It''s the most wonderful time of the year','its the most wonderful time of the year', 'Scott Joe')""")

cur.execute("""CREATE TABLE songs ( id INTEGER PRIMARY KEY AUTOINCREMENT,
            song_name TEXT UNIQUE NOT NULL,
            song_author TEXT NOT NULL,
            song_img_path TEXT NOT NULL,
            song_mp3_path TEXT NOT NULL,
            song_txt_path TEXT NOT NULL,
            song_duration_secs INT,
            song_duration_mins TEXT,
            likes INTEGER DEFAULT 0)""")

cur.execute("""INSERT INTO songs (song_name, song_author, song_img_path, song_mp3_path, song_txt_path, song_duration_secs, song_duration_mins) VALUES (
    'Kazdy den budu vraj Vianoce',
    'Miroslav Zbirka',
    'song_imgs/1.jpg', 
    'songs_mp3/1.mp3', 
    'seq_txt/1.txt',
    '132',
    '2:12'
    )
""")

cur.execute("""INSERT INTO songs (song_name, song_author, song_img_path, song_mp3_path, song_txt_path, song_duration_secs, song_duration_mins) VALUES (
    'Podme bratia do Betlema',
    'Tublatanka',
    'song_imgs/2.jpg', 
    'songs_mp3/2.mp3', 
    'seq_txt/2.txt',
    '103',
    '1:52')
""")

cur.execute("""INSERT INTO songs (song_name, song_author, song_img_path, song_mp3_path, song_txt_path, song_duration_secs, song_duration_mins) VALUES (
    'Let It Go',
    'Indina Menzel',
    'song_imgs/3.jpg', 
    'songs_mp3/3.mp3', 
    'seq_txt/3.txt',
    '156',
    '2:36')
""")

cur.execute("""INSERT INTO songs (song_name, song_author, song_img_path, song_mp3_path, song_txt_path, song_duration_secs, song_duration_mins) VALUES (
    'Christmas Lights',
    'Coldplay',
    'song_imgs/4.jpg', 
    'songs_mp3/4.mp3', 
    'seq_txt/4.txt',
    '102',
    '1:42')
""")

cur.execute("""INSERT INTO songs (song_name, song_author, song_img_path, song_mp3_path, song_txt_path, song_duration_secs, song_duration_mins) VALUES (
    'Medvidek',
    'Lucie',
    'song_imgs/5.jpg', 
    'songs_mp3/5.mp3', 
    'seq_txt/5.txt',
    '232',
    '3:52')
""")

cur.execute("""INSERT INTO songs (song_name, song_author, song_img_path, song_mp3_path, song_txt_path, song_duration_secs, song_duration_mins) VALUES (
    'Santa Claus is coming to town',
    'Mariah Carey',
    'song_imgs/6.jpg', 
    'songs_mp3/6.mp3', 
    'seq_txt/6.txt',
    '246',
    '3:06')
""")

cur.execute("""INSERT INTO songs (song_name, song_author, song_img_path, song_mp3_path, song_txt_path, song_duration_secs, song_duration_mins) VALUES (
    'Biela zima',
    'Michal Docolomansky',
    'song_imgs/7.jpg', 
    'songs_mp3/7.mp3', 
    'seq_txt/7.txt',
    '198',
    '3:18')""")


    
conn.commit()

conn.close()
