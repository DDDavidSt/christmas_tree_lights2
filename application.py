from flask import Flask, url_for, jsonify, render_template, request, send_from_directory , url_for, flash, redirect, session
from flask_session import Session


import os
import random
import subprocess
from werkzeug.utils import secure_filename
from PIL import Image
import re
import sqlite3
from mutagen.mp3 import MP3
import alsaaudio

import multiprocessing
import play_songs

cmd = "mkdir trash_mp3 && mkdir trash_txt && mkdir trash_img"
os.system(cmd)

UPLOAD_FOLDER_IMG = os.path.abspath('static/song_imgs')
UPLOAD_FOLDER_MP3 = os.path.abspath('songs_mp3')
UPLOAD_FOLDER_TXT = os.path.abspath('seq_txt')
ALLOWED_EXTENSIONS = {'txt', 'mp3', 'png', 'jpg', 'jpeg'}


DATABASE_PATH = os.path.abspath('chtrli.db')
print('db path:',DATABASE_PATH)
print('upload img folder', UPLOAD_FOLDER_IMG)
print('upload mp3 folder', UPLOAD_FOLDER_MP3)
print('upload txt folder', UPLOAD_FOLDER_TXT)
currsong_index = 4

errors = []
success = []
values = None

login_errors = []
signup_errors = [] 


app = Flask(__name__)
app.config['UPLOAD_FOLDER_IMG'] = UPLOAD_FOLDER_IMG
app.config['UPLOAD_FOLDER_MP3'] = UPLOAD_FOLDER_MP3
app.config['UPLOAD_FOLDER_TXT'] = UPLOAD_FOLDER_TXT
app.config['SECRET_KEY'] = '3bd37c56bd8f439c4eb8b5ad3030eaf5abf550f6d522b3d3'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

@app.route('/playsong/<id>')
def playsong(id):
    global d
    if int(id) in d['songs'].keys():
        d['currsec'] = 0
        d['currsong'] = int(id)

    return redirect(request.referrer)

@app.route("/edit", methods=["GET", "POST"])
def edit():
    global errors, success,d
    if session.get('admin') == 1:
        errors = []
        success = []

        cur_ret = opendb(DATABASE_PATH)

        if cur_ret is None:
            errors.append("Failed to connect to the database")
            return redirect("error")
        else:
            conn, cur = cur_ret
            conn.row_factory = sqlite3.Row

        succ_mess = ''
        if request.method == "POST":
            if d['currsong']== int(request.form['id']):
                errors.append("You cannot edit a song that is currently playing")
                return redirect("adm_pl")

            if 'song_name' in request.form:
                name = check_name(request.form["song_name"])
                if len(name) != 0:
                    try:
                        cur.execute("UPDATE songs SET song_name=? WHERE id=?", (name, int(request.form['id'])))
                        succ_mess += f'Song <strong>{name}</strong> ';
                    except:
                        errors.append("There was a problem with writing to the database: check if the name is unique")
                        return redirect("adm_pl")

                else:
                    errors.append("Empty or not permitted song name")

            if 'song_author' in request.form:
                auth = check_name(request.form["song_author"])
                if len(auth) != 0:
                    try:
                        cur.execute("UPDATE songs SET song_author=? WHERE id=?", (auth, int(request.form['id'])))
                        succ_mess += f'by <strong>{auth}</strong> '
                    except:
                        errors.append("There was a problem with writing into the databse: check the author")
                        return redirect("adm_pl")
                else:
                    errors.append("Empty or not permitted song author")
            
            if check_if_in_database(name, auth, request.form['id']):
                errors.append("Such song name associated with given author is already in the database")
                return redirect("adm_pl")
            
            if 'song_img' in request.files and request.files["song_img"].filename != '':
                file = request.files['song_img']

                if file and allowed_file(file.filename):
                    
                    filename = secure_filename(file.filename)
                    try:
                        im = Image.open(file)
                        resized = im.resize((180,180))
                        resized.save(os.path.join(app.config["UPLOAD_FOLDER_IMG"], request.form['id']+ '.jpg'), 'JPEG')
                    except Exception as e:
                        errors.append("There was a problem with uploading the image - check the image mode (not rgba) and file extension")
                        errors.append("<strong>Details:</strong>")
                        errors.append("<code>"+str(e)+"</code>")
                        return redirect("adm_pl")

                    try:
                        cur.execute("UPDATE songs SET song_img_path=? WHERE id=?", (os.path.join('song_imgs/', request.form['id'] + '.jpg'), int(request.form['id'])))
                        succ_mess += f'with chosen img file <strong>{filename}</strong> '
                    except:
                        errors.append("There was a problem with writing into the database: check the chosen image")

                        return redirect("adm_pl")
                else:
                    errors.append("File extension not permitted or wrong file name")
            
            if 'mp3_song' in request.files and request.files["mp3_song"].filename != '':
                mp3_file = request.files['mp3_song']
                if mp3_file.filename[-4:] != '.mp3':
                    errors.append("Wrong mp3 file extension: only .mp3 allowed")
                if mp3_file and allowed_file(mp3_file.filename):
                    
                    mp3_filename = secure_filename(mp3_file.filename)
                    try:
                        mp3_file.save(os.path.join(app.config["UPLOAD_FOLDER_MP3"], mp3_filename+ '.mp3'))               
                    except Exception as e:
                        errors.append("There was a problem with uploading the mp3 file - check the file extension")
                        errors.append("<strong>Details:</strong><br><code>"+str(e)+"</code>")
                        return redirect("adm_pl")
                    succ_mess += f', mp3 file <strong>{mp3_filename}</strong>'
                    song_duration = get_song_duration(os.path.join(app.config["UPLOAD_FOLDER_MP3"], mp3_filename+ '.mp3'))
                    try:
                        cur.execute("UPDATE songs SET song_mp3_path=?, song_duration_secs=? WHERE id=?", (os.path.join(app.config["UPLOAD_FOLDER_MP3"], mp3_filename + '.mp3'), song_duration, int(request.form['id'])))
                        succ_mess += f'with chosen img file <strong>{mp3_filename}</strong> '
                    except sqlite3.Error as e:
                        errors.append("There was a problem with writing into the database: <code>"+str(e)+"</code>")

                        return redirect("adm_pl")
                else:
                    errors.append("File extension not permitted or wrong mp3 file name")
                

            if 'txt_sequence' in request.files and request.files["txt_sequence"].filename != '':
                txt_file = request.files['txt_sequence']
                if txt_file.filename[-4:] != '.txt':
                    errors.append("Wrong txt file extension: only .txt allowed")
                if txt_file and allowed_file(txt_file.filename):
                    txt_filename = secure_filename(txt_file.filename)
                    try:
                        txt_file.save(os.path.join(app.config["UPLOAD_FOLDER_TXT"], txt_filename))
                    except Exception as e:
                        errors.append("There was a problem with uploading the txt sequence - check the file extension")
                        errors.append("<strong>Details:</strong>")
                        errors.append("<code>"+str(e)+"</code>")
                        return redirect("adm_pl")
                    try:
                        print(os.path.join(app.config["UPLOAD_FOLDER_TXT"], txt_filename))
                        cur.execute("UPDATE songs SET song_txt_path=?  WHERE id=?", (os.path.join(app.config["UPLOAD_FOLDER_TXT"], txt_filename),int(request.form['id'])))
                        succ_mess += f'with chosen txt file <strong>{txt_filename}</strong> '
                    except sqlite3.Error as e:
                        errors.append("There was a problem with writing into the database: <code> "+ str(e)+ "</code>")

                        return redirect("adm_pl")
                    succ_mess += f', txt sequence file <strong>{txt_filename}</strong> '
                    
                else:
                    errors.append("File extension not permitted or wrong file name")
                
        if not errors:
            conn.commit()
            if succ_mess != '':
                success.append(succ_mess+'was edited')
        
        return redirect("adm_pl")
    else:
        songs=get_songs()
        return render_template("unauthorised.html", currson_index=d['currsong'], currsong=songs[d['songs'][d['currsong']][0]], songs=songs)

@app.route("/add_new", methods=["GET", "POST"])
def add_new():
    global errors, success, values
    if session.get('admin') == 1:
        errors = []
        success = []

        cur_ret = opendb(DATABASE_PATH)

        if cur_ret is None:
            errors.append("Failed to connect to the database")
            return redirect("error")
        else:
            conn, cur = cur_ret
            conn.row_factory = sqlite3.Row

        succ_mess = ''
        if request.method == "POST":
            values = (request.form.to_dict())

            #find the last id from songs table - the ne file is gonna have id + 1
            cur.execute("SELECT seq FROM sqlite_sequence WHERE name='songs';")
            next_id = '1'
            try:
                next_id = str(list(cur.fetchone())[0] + 1)
            except:
                pass
            if 'song_name_new' in request.form:
                name = check_name(request.form["song_name_new"])
                if len(name) != 0:
                    succ_mess += f'Song <strong>{name}</strong> '
                else:
                    errors.append("Empty or not permitted song name")
            else:
                errors.append("Song name is a required input field!")

            if 'song_author_new' in request.form:
                auth = check_name(request.form["song_author_new"])
                if len(auth) != 0:
                    succ_mess += f'by <strong>{auth}</strong> '
                else:
                    errors.append("Empty or not permitted song author")
            else:
                errors.append("Song author is a required input field!")

            if 'song_img_new' in request.files and request.files["song_img_new"].filename != '':
                img_file = request.files['song_img_new']
                if img_file.filename[-4:] != '.jpg' and img_file.filename[-4:] != '.png':
                    errors.append("Wrong img file extension: only .jpg or .png allowed")
                if img_file and allowed_file(img_file.filename):
                    
                    img_filename = secure_filename(img_file.filename)
                    
                else:
                    errors.append("File extension not permitted or wrong file name")
            else:
                errors.append("Song image is a required input field")

            if 'mp3_song_new' in request.files and request.files["mp3_song_new"].filename != '':
                mp3_file = request.files['mp3_song_new']
                if mp3_file.filename[-4:] != '.mp3':
                    errors.append("Wrong mp3 file extension: only .mp3 allowed")
                if mp3_file and allowed_file(mp3_file.filename):
                    
                    mp3_filename = secure_filename(mp3_file.filename)
                    
                else:
                    errors.append("File extension not permitted or wrong mp3 file name")
            else:
                errors.append("MP3 file is a required input field")

            if 'txt_sequence_new' in request.files and request.files["txt_sequence_new"].filename != '':
                txt_file = request.files['txt_sequence_new']
                if txt_file.filename[-4:] != '.txt':
                    errors.append("Wrong txt file extension: only .txt allowed")
                if txt_file and allowed_file(txt_file.filename):
                    
                    txt_filename = secure_filename(txt_file.filename)
                    
                else:
                    errors.append("File extension not permitted or wrong file name")
            else:
                errors.append("TXT sequence is a required input field")
        if check_if_in_database(name, auth):
                errors.append("Such song name associated with given author is already in the database")
        if errors != []:
            succ_mess = ''
            return redirect("adm_pl")
        try:
            #saving the files
            img_path = os.path.join(app.config["UPLOAD_FOLDER_IMG"], next_id+ '.jpg')
            try:
                im = Image.open(img_file)
                resized = im.resize((180,180))
                resized.save(img_path, 'JPEG')
            except Exception as e:
                errors.append("There was a problem with uploading the image - check the image mode (not rgba) and file extension")
                errors.append("<strong>Details:</strong>")
                errors.append("<code>"+str(e)+"</code>")
                return redirect("adm_pl")

            
            succ_mess += f'with chosen img file <strong>{img_filename}</strong>'
            mp3_path = os.path.join(app.config["UPLOAD_FOLDER_MP3"], next_id+ '.mp3')     
            try:
                mp3_file.save(mp3_path)               
            except Exception as e:
                errors.append("There was a problem with uploading the mp3 file - check the image mode (not rgba) and file extension")
                errors.append("<strong>Details:</strong><br><code>"+str(e)+"</code>")
                return redirect("adm_pl")
            succ_mess += f', mp3 file <strong>{mp3_filename}</strong>'
            song_duration = get_song_duration(mp3_path)

            txt_path = os.path.join(app.config["UPLOAD_FOLDER_TXT"], next_id+ '.txt')
            try:
                txt_file.save(txt_path)
            except Exception as e:
                errors.append("There was a problem with uploading the txt sequence - check the file extension")
                errors.append("<strong>Details:</strong>")
                errors.append("<code>"+str(e)+"</code>")
                return redirect("adm_pl")
            succ_mess += f', txt sequence file <strong>{txt_filename}</strong> '
                
            cur.execute("INSERT INTO songs (song_name, song_author, song_img_path, song_mp3_path, song_txt_path, song_duration_secs, song_duration_mins) VALUES (?,?,?,?,?,?,?)"
            ,(name, auth, 'song_imgs/'+next_id + '.jpg', mp3_path, txt_path, song_duration, sec_to_mins_sec(song_duration)))
            conn.commit()
        except Exception as e:
            errors.append("There was problem with writing into the database - check if all input fields are correctly filled and try again")
            errors.append("Details: <br>" + str(e))
            return redirect("adm_pl")

        if succ_mess != '':
            success.append(succ_mess+'was added.')
            cur.execute("SELECT id,song_mp3_path, song_txt_path, song_name, song_duration_secs FROM songs")
            song_list = list(cur.fetchall())
            sdict = {}
            for i in song_list:
                sdict[i[0]] = i
            d['songs'] = sdict


        return redirect("adm_pl")
    else:
        songs=get_songs()
        return render_template("unauthorised.html", currson_index=d['currsong'], currsong=songs[d['songs'][d['currsong']][0]], songs=songs)


@app.route('/volume')
def volume():
    m = alsaaudio.Mixer("Headphone")
    return jsonify({'vol': m.getvolume()})

@app.route('/set_vol', methods=['POST', 'GET'])
def set_volume():
    if session.get('id') is not None:
        if request.method == "POST":
            m = alsaaudio.Mixer("Headphone")
            m.setvolume(int(request.values.get("vol")))   
        return redirect(url_for("home"))
    else:
        return 'cannot set volume - no logged in user'

@app.route("/make_adm", methods=["POST", "GET"])
def make_admin():
    if session.get('id') is not None and session.get('admin') == 1:
        uid = request.values.get("id")

        cur_ret = opendb(DATABASE_PATH)

        if cur_ret is None:
            print("Failed to connect to the database")
            return jsonify(error=True), 400
        else:
            conn, cur = cur_ret
            conn.row_factory = sqlite3.Row
        try:
            cur.execute("UPDATE users SET admin=1 WHERE id=?", (uid,))
            conn.commit()
            return jsonify(success=True)
        except sqlite3.Error as e:

            return jsonify(error=True), 400
    else:
        return jsonify(error=True), 400

@app.route("/undo_adm", methods=["POST", "GET"])
def undo_admin():
    if session.get('id') is not None and session.get('admin') == 1:
        uid = request.values.get("id")
        cur_ret = opendb(DATABASE_PATH)

        if cur_ret is None:
            print("Failed to connect to the database")
            return jsonify(error=True), 400
        else:
            conn, cur = cur_ret
            conn.row_factory = sqlite3.Row
        try:
            cur.execute("UPDATE users SET admin=0 WHERE id=?", (uid,))
            conn.commit()
            return jsonify(success=True)
        except sqlite3.Error as e:
            return jsonify(error=True), 400
    else:
        return jsonify(error=True), 400


@app.route("/like_song", methods=["POST", "GET"])
def like_song():
    if session.get('id') is not None:
        sid = request.values.get("id")
        cur_ret = opendb(DATABASE_PATH)

        if cur_ret is None:
            errors.append("Failed to connect to the database")
            return redirect("error")
        else:
            conn, cur = cur_ret
            conn.row_factory = sqlite3.Row
        try:
            cur.execute("INSERT INTO likes_songs (uid, song_id) VALUES (?, ?)", (session.get('id'), sid))
            cur.execute("UPDATE songs SET likes = likes + 1 WHERE id=?", (sid,))
            conn.commit()
        except sqlite3.Error as e:
            pass
    else:
        songs=get_songs()
        return render_template("unauthorised.html", currson_index=d['currsong'], currsong=songs[d['songs'][d['currsong']][0]], songs=songs)


@app.route("/unlike_song", methods=["POST", "GET"])
def unlike_song():
    if session.get('id') is not None:
        sid = request.values.get("id")
        cur_ret = opendb(DATABASE_PATH)

        if cur_ret is None:
            errors.append("Failed to connect to the database")
            return redirect("error")
        else:
            conn, cur = cur_ret
            conn.row_factory = sqlite3.Row
        try:
            cur.execute("DELETE FROM likes_songs WHERE uid=? AND song_id=?", (session.get('id'), sid))
            cur.execute("UPDATE songs SET likes = likes - 1 WHERE id=?", (sid,))

            conn.commit()
        except sqlite3.Error as e:
            pass
    else:
        songs=get_songs()
        return render_template("unauthorised.html", currson_index=d['currsong'], currsong=songs[d['songs'][d['currsong']][0]], songs=songs)


@app.route("/like_sugg", methods=["POST", "GET"])
def like_sugg():
    if session.get('id') is not None:
        sid = request.values.get("id")
        cur_ret = opendb(DATABASE_PATH)

        if cur_ret is None:
            errors.append("Failed to connect to the database")
            return redirect("error")
        else:
            conn, cur = cur_ret
            conn.row_factory = sqlite3.Row
        try:
            cur.execute("INSERT INTO likes_sugg (uid, sugg_id) VALUES (?, ?)", (session.get('id'), sid))
            cur.execute("UPDATE suggestions SET likes = likes + 1 WHERE id=?", (sid,))
            conn.commit()
        except sqlite3.Error as e:
            pass
    else:
        songs=get_songs()
        return render_template("unauthorised.html", currson_index=d['currsong'], currsong=songs[d['songs'][d['currsong']][0]], songs=songs)


@app.route("/unlike_sugg", methods=["POST", "GET"])
def unlike_sugg():
    if session.get('id') is not None:
        sid = request.values.get("id")
        cur_ret = opendb(DATABASE_PATH)

        if cur_ret is None:
            errors.append("Failed to connect to the database")
            return redirect("error")
        else:
            conn, cur = cur_ret
            conn.row_factory = sqlite3.Row
        try:
            cur.execute("DELETE FROM likes_sugg WHERE uid=? AND sugg_id=?", (session.get('id'), sid))
            cur.execute("UPDATE suggestions SET likes = likes - 1 WHERE id=?", (sid,))
            conn.commit()
        except sqlite3.Error as e:
            pass
    else:
        songs=get_songs()
        return render_template("unauthorised.html", currson_index=d['currsong'], currsong=songs[d['songs'][d['currsong']][0]], songs=songs)

@app.route("/adm_usrs")
def adm_usrs():
    global currsong_index
    if session.get('admin') == 1:
        songs = get_songs()
        cur_ret = opendb(DATABASE_PATH)

        if cur_ret is None:
            errors.append("Failed to connect to the database")
            return redirect("error")
        else:
            conn, cur = cur_ret
            conn.row_factory = sqlite3.Row
        
        res = cur.execute("SELECT * FROM users")
        
        usrs = []
        for row in  cur.fetchall():
            col_names = [tup[0] for tup in res.description]
            row_val = [i for i in row]
            usrs.append(dict(zip(col_names,row_val)))
        if len(songs) > 0:
            return render_template("adm_users.html", songs=songs, currsong=songs[d['songs'][d['currsong']][0]], usrs=usrs)
        if songs == {}:
            return render_template("adm_users.html", songs=songs, currsong="Empty song list", usrs=usrs)

    else:
        songs=get_songs()
        return render_template("unauthorised.html", currson_index=d['currsong'], currsong=songs[d['songs'][d['currsong']][0]], songs=songs)
    errors.append("Failed to connect to the database")
    return redirect("error")

@app.route('/adm_pl/delete/<id>', methods=["POST"])
def del_song(id):
    global success, errors
    print(id, d['currsong'])
    if( str(d['currsong']) == id and len(d['songs']) > 1):
        errors.append("Cannot delete a song that is being played")
        return redirect(url_for('admin_playlist')) 

    if session.get('admin') == 1:
        cur_ret = opendb(DATABASE_PATH)

        if cur_ret is None:
            errors.append("Failed to connect to the database")
            return redirect("error")
        else:
            conn, cur = cur_ret
            conn.row_factory = sqlite3.Row
        try:
            
            
            song = get_song(id)
            cmd = f"mv songs_mp3/{song[0]['id']}.mp3 trash_mp3/"
            os.system(cmd)
            cmd = f"mv seq_txt/{song[0]['id']}.txt trash_txt/"
            os.system(cmd)
            cmd = f"mv static/song_imgs/{song[0]['id']}.jpg trash_img/"
            os.system(cmd)
            cur.execute("DELETE FROM songs WHERE id=?", (int(id),))
            conn.commit()
        except Exception as e:
            errors.append("Error deleting from the database<br>Details:<br>"+str(e))
        success.append("Selected song was successfully deleted")
        cur.execute("SELECT id,song_mp3_path, song_txt_path, song_name, song_duration_secs FROM songs")
        song_list = list(cur.fetchall())
        sdict = {}
        for i in song_list:
            sdict[i[0]] = i
        d['songs'] = sdict
        return redirect(url_for('admin_playlist')) 
    else:
        songs=get_songs()
        return render_template("unauthorised.html", currson_index=d['currsong'], currsong=songs[d['songs'][d['currsong']][0]], songs=songs)

@app.route('/seconds-full_length')
def get_currsong():
    global d
    # print(d)
    return jsonify({'secs': (d['currsecs']),  'song': get_song(d['currsong'])})

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/playlist')
def playlist():
    global errors
    songs = get_songs()
    if len(songs) > 0 :
        if(d['currsong'] not in d['songs'].keys() and len(d['songs']) < 2):
            d['currsong'] = min(d['songs'].keys())
        return render_template("playlist.html", songs=songs,  currsong_index=d['currsong'], currsong=d['songs'][d['currsong']])
    if songs == {}:
        return render_template("playlist.html", songs={0:{"song_name":"Empty song list", "song_author":"nothing to play"}},  currsong_index=0, currsong=())
    return redirect("error")

@app.route('/adm_pl', methods=["GET", "POST"])
def admin_playlist():
    
    global errors, success, values #prevent showing errors, success messages to other users
    if session.get('admin') == 1:

        nowerrors = errors.copy()
        nowsuccess = success.copy()
        nowvalues = None
        if values is not None:
            nowvalues = values.copy()

        errors = []
        success = []
        songs = get_songs()
        if len(songs) != 0:
            print(d)
            if(d['currsong'] not in d['songs'].keys() and len(d['songs']) < 2):
                d['currsong'] = min(d['songs'].keys())
            return render_template("adm_playlist.html", songs=songs, currsong_index=d['currsong'], currsong=d['songs'][d['currsong']], errors=nowerrors, success=nowsuccess, form_val=nowvalues)
        if songs == {}:
            errors.append("Empty song list")
            return render_template("adm_playlist.html", songs={}, curssong_index =0,errors=nowerrors,currsong="empty", success=nowsuccess, form_val=nowvalues )
    else:
        songs=get_songs()
        if len(songs) > 0:
            return render_template("unauthorised.html",  currsong_index=d['currsong'], currsong=d['songs'][d['currsong']], songs=songs)
        if songs == {}:
            errors.append("Empty song list")
            return render_template("adm_playlist.html", songs={}, curssong_index =0,errors=nowerrors,currsong="empty", success=nowsuccess, form_val=nowvalues )
    errors.append("Empty song list")
    return redirect("error")
@app.route('/login', methods=['POST', 'GET'])
def login():
    global login_errors
    login_errors = []

    if request.method == "POST":
        cur_ret = opendb(DATABASE_PATH)

        if cur_ret is None:
            errors.append("Failed to connect to the database")
            return redirect("error")
        else:
            conn, cur = cur_ret
            conn.row_factory = sqlite3.Row

        res = cur.execute("SELECT * FROM users WHERE uname=? AND pswd=?", (request.form.get('uname').strip(), request.form.get('pswd')))
        row = cur.fetchall()
        if row == []:
            login_errors.append("Wrong username or password")
        else:
            col_names = [tup[0] for tup in res.description]
            row_val = [i for i in row[0]]
            usr = dict(zip(col_names,row_val))

            session["name"] = usr['uname']
            session['id'] = int(usr['id'])
            session['admin'] = int(usr['admin'])
   
    return redirect('/')

@app.route('/account')
def my_account():
    global errors, success
    if session.get('id') is not None:
        nowerrors, nowsuccess = errors.copy(), success.copy()
        errors, success = [], []
        songs = get_songs()
        if len(songs) > 0:
            suggestions = get_suggestions(session.get('id', -1))
            return render_template('account.html', currsong_index=d['currsong'], currsong=d['songs'][d['currsong']], errors=nowerrors, success=nowsuccess, suggestions=suggestions)
        if songs == {}:
            suggestions = get_suggestions(session.get('id', -1))
            return render_template('account.html', currsong_index=0, currsong="Empty song list", errors=nowerrors, success=nowsuccess, suggestions=suggestions)
        
    else:
        songs=get_songs()
        if len(songs) > 0:
            return render_template("unauthorised.html", currson_index=d['currsong'], currsong=d['songs'][d['currsong']], songs=songs)
        if songs == {}:
            return render_template("unauthorised.html", currson_index=0, currsong="Empty song list", songs=songs)

    errors.append("Empty song list")
    return redirect("error")
        
@app.route("/account/delete_sugg/<id>")
def delete_sugg(id):
    global errors, success

    if session.get('id') is not None:
        usr_sugg = get_suggestions(session['id'])
        usrs_ids = [ sugg['id'] for sugg in usr_sugg]#to check if the user is deleting only their suggestions
        if int(id) in usrs_ids:
            cur_ret = opendb(DATABASE_PATH)

            if cur_ret is None:
                errors.append("Failed to connect to the database")
                return redirect("error")
            else:
                conn, cur = cur_ret
                conn.row_factory = sqlite3.Row
            
            try:
                cur.execute("DELETE from suggestions WHERE id=?", (int(id),))
                conn.commit()
                deleted = list(filter(lambda x: x['id'] == int(id), usr_sugg))
                success.append(f"Suggestion of a song <strong>{deleted[0]['song_name']}</strong> by <strong>{deleted[0]['song_author']}</strong> was deleted")

            except sqlite3.Error:
                errors.append("There was a problem with writing into the database")
        else:
            errors.append("You are not permitted to delete this suggestion or this suggestion does not exist anymore")
        return redirect(url_for('my_account'))
    else:
        songs=get_songs()
        return render_template("unauthorised.html", currson_index=d['currsong'], currsong=songs[d['songs'][d['currsong']][0]], songs=songs)

@app.route('/chng_account', methods=["POST", "GET"])
def change_acc():
    global errors, success
    if session.get('id') is not None:
        if request.method == "POST":
            cur_ret = opendb(DATABASE_PATH)

            if cur_ret is None:
                errors.append("Failed to connect to the database")
                return redirect("error")
            else:
                conn, cur = cur_ret
                conn.row_factory = sqlite3.Row

            name = check_name(request.form['usr_name'].strip())
            succ_mess = ''
            #checking if new name is already in the database
            try:
                cur.execute("SELECT * FROM users WHERE uname=? AND id!=?", (name,session.get('id')))
            except:
                errors.append("Error reading from database")
            if cur.fetchall() != []:
                errors.append("Username already exists")
            elif len(name) < 3:#checking correct length
                errors.append("Username must be at least 3 characters long")
            else:
                succ_mess += f"You successfully changed your name to <strong>{name}</strong> "
            if 'old_pswd' in request.form:
                old = request.form.get('old_pswd')
                
                cur.execute("SELECT * FROM users WHERE uname=? AND pswd=?", (session['name'],old))
                if cur.fetchall() == []:
                    errors.append("Provided password is incorrect")
                if 'new_pswd' in request.form:
                    new = request.form.get('new_pswd')
                else:
                    errors.append("New password input field cannot be empty")
                if 'new_pswd_agn' in request.form:
                    new_agn = request.form.get('new_pswd_agn')
                else:
                    errors.append("You have to repeat the new password")
                if len(new) < 6:
                    errors.append("New password must be at least 6 characters long")
                if new != new_agn:
                    errors.append("Passwords do not match")
                if len(errors) == 0:
                    try:
                        cur.execute("UPDATE users SET uname=?, pswd=? WHERE uname=?", (name , new , session['name']))
                        if cur.rowcount == 1:
                            conn.commit()
                            succ_mess += "with a password modification"
                            success.append(succ_mess)
                            session['name'] = name
                    except (sqlite3.Error, sqlite3.IntegrityError) as e:
                        errors.append("Problem when writing into database - user does not exist anymore or given username is not unique")
            else:
                if len(errors) == 0:
                    try:
                        cur.execute("UPDATE users SET uname=? WHERE uname=? ", (name, session['name']))
                        if cur.rowcount == 1:
                            conn.commit()
                            succ_mess += "without any password modification"
                            success.append(succ_mess)
                            session['name'] = name
                    except (sqlite3.Error, sqlite3.IntegrityError) as e:
                        errors.append("Problem when writing into database - user does not exist anymore or given username is not unique (try logging out and in)")
            return redirect('account')
    else:
        songs=get_songs()
        return render_template("unauthorised.html", currson_index=d['currsong'], currsong=songs[d['songs'][d['currsong']][0]], songs=songs)

@app.route('/signup', methods=['POST', 'GET'])
def sign_up():
    global signup_errors
    sign_up_errors = []

    if request.method == "POST":
        #check if name is unique
        cur_ret = opendb(DATABASE_PATH)

        if cur_ret is None:
                errors.append("Failed to connect to the database")
                return redirect("error")
        else:
            conn, cur = cur_ret
            conn.row_factory = sqlite3.Row

        new_usr_name = check_name(request.form.get('uname'))
        if len(new_usr_name) < 3:
            signup_errors.append("Username must be at least 3 characters long and has to be of a standard username format (no special characters")         
            return redirect('/')

        new_usr_pswd = request.form.get('pswd')

        if len(new_usr_pswd) < 6:
            signup_errors.append("Password must be at least 6 characters long")
            return redirect('/')
        
        cur.execute("SELECT * FROM users WHERE uname=?", (new_usr_name,))
        row = cur.fetchall()
        if row == []:
            if new_usr_pswd == request.form.get('pswd_agn'):
                try:
                    cur.execute("INSERT INTO users (uname, pswd) VALUES (?,?)", (new_usr_name, new_usr_pswd))
                except:
                    signup_errors.append("There was a problem writing into the database - check if the username and password are of the correct format")
                conn.commit()
                session["name"] = new_usr_name
                session['id'] = cur.lastrowid
                session['admin'] = 0
                conn.commit()
            else:
                signup_errors.append("Provided passwords do not match")
        else:
            signup_errors.append("Username with such name already exists")
        return redirect('/')

@app.route('/logout')
def logout():
    try:
        session["name"] = None
        session["id"] = None
        session['admin'] = None
    except:
        pass
    return redirect('/')

@app.route("/")
def index():
    global login_errors, signup_errors,d
    now_login_errors = login_errors.copy()
    now_sgp_errors = signup_errors.copy()
    login_errors = []
    signup_errors = []

    now_log_err = login_errors.copy()
    login_errors = []
    if d['songs']:
        return render_template("index.html", currsong=d['songs'][d['currsong']], login_errors=now_login_errors, signup_errors=now_sgp_errors)
    else:
        return render_template("index.html", currsong=0, login_errors=now_login_errors, signup_errors=now_sgp_errors)
    return redirect("error")

@app.route("/next")
def next():
    global d
    ids = list(d['songs'].keys())
    curid = ids.index(d['currsong'])
    if curid + 1 >= len(ids):
        d['currsong'] = min(d['songs'].keys())
    else:
        d['currsong'] = ids[curid+1]
    d['currsec'] = 0
    return redirect(request.referrer)

@app.route("/prev")
def prev():
    global d
    ids = list(d['songs'].keys())
    curid = ids.index(d['currsong'])
    if curid-1  < 0:
        d['currsong'] =  max(d['songs'].keys())
    else:
        d['currsong'] = ids[curid-1]
    d['currsec'] = 0

    return redirect(request.referrer)

@app.route("/home")
def home():
    return redirect('/')

@app.route('/suggestions')
def suggestions():
    global errors, success
    nowerrors = errors.copy()
    nowsuccess = success.copy()
    errors, success = [], []

    songs = get_songs()
    if len(songs) > 0:
        suggestions = get_suggestions()
        return render_template("suggestions.html", currsong=d['songs'][d['currsong']], usr_suggestions=suggestions, errors=nowerrors, success=nowsuccess)
    if songs == {}:
        suggestions = get_suggestions()
        return render_template("suggestions.html", currsong="Empty song list", usr_suggestions=suggestions, errors=nowerrors, success=nowsuccess)
    errors.append("Failed to connect to the database")
    return redirect("error")


@app.route('/adm_sugg')
def adm_suggestions():
    global errors, success
    if session.get('admin') == 1:
        nowerrors = errors.copy()
        nowsuccess = success.copy()
        errors, success = [], []
        songs = get_songs()
        if len(songs) > 0:
            suggestions = get_suggestions()
            return render_template("adm_suggestions.html", currsong=songs[d['songs'][d['currsong']][0]], suggestions=suggestions, errors=nowerrors, success=nowsuccess)
        if songs == {}:
            suggestions = get_suggestions()
            return render_template("adm_suggestions.html", currsong="Empty song list", suggestions=suggestions, errors=nowerrors, success=nowsuccess)
        errors.append("Failed to connect to the database")
        return redirect("error")
    else:
        songs=get_songs()
        if songs:
            return render_template("unauthorised.html", currson_index=d['currsong'], currsong=songs[d['songs'][d['currsong']][0]], songs=songs)
        if songs == {}:
            errors.append("Empty suggestions list")
            return render_template("adm_suggestions.html", currsong="Empty song list", suggestions=suggestions, errors=nowerrors, success=nowsuccess)
          
        errors.append("Failed to connect to the database")
        return redirect("error")

@app.route("/adm_sugg/delete_sugg/<id>")
def adm_delete_sugg(id):
    global errors, success
    if session.get('admin') == 1:
        cur_ret = opendb(DATABASE_PATH)

        if cur_ret is None:
                errors.append("Failed to connect to the database")
                return redirect("error")
        else:
            conn, cur = cur_ret
            conn.row_factory = sqlite3.Row
        
        try:
            res = cur.execute("SELECT * FROM suggestions WHERE id=?", (int(id),))
            deleted= []
            for row in  cur.fetchall():
                col_names = [tup[0] for tup in res.description]
                row_val = [i for i in row]
                deleted.append(dict(zip(col_names,row_val)))
                
            cur.execute("DELETE from suggestions WHERE id=?", (int(id),))
            conn.commit()
            for delitem in deleted:
                success.append(f"Suggestion of a song <strong>{delitem['song_name']}</strong> by <strong>{delitem['song_author']}</strong> was deleted by <strong> ADMIN </strong>")

        except sqlite3.Error:
            errors.append("There was a problem with writing into the database")
    else:
        errors.append("You are not permitted to delete this suggestion or this suggestion does not exist anymore")
    return redirect(url_for('adm_suggestions'))

@app.route('/add_sugg', methods=["POST", "GET"])
def add_suggestion():
    global errors, success
    errors, success = [], []
    cur_ret = opendb(DATABASE_PATH)

    if cur_ret is None:
        errors.append("Failed to connect to the database")
        return redirect("error")
    else:
        conn, cur = cur_ret
        conn.row_factory = sqlite3.Row
    
    name, author, succ_mess = '','',''
    uid = session.get('id')
    #if noone is logged in
    if uid is None:
        uid = 0

    if request.method == "POST":
        if 'sugg_name' in request.form:
            name = check_name(request.form["sugg_name"])
            if len(name) != 0:
                    succ_mess += f'Song <strong>{name}</strong> ';
            else:
                errors.append("Empty or not permitted song name")
        if 'sugg_author' in request.form:
            author = check_name(request.form["sugg_author"])
            if len(name) != 0:
                    succ_mess += f'by <strong>{author}</strong> ';
            else:
                errors.append("Empty or not permitted author text")
        if name == '' or author == '':
            errors.append("Suggested song name or author cannot be empty")
        else:
            try:
                #check if such a song isn't already in the database
                name_std = rplc_spcl_char(name) #tries to crop the name as much as possible

                cur.execute("SELECT * FROM suggestions WHERE name_std=?", (name_std,))
                rslt = cur.fetchall()
                if rslt != []:
                    errors.append(f"This song appears to be in the suggestions already. Did you mean <strong>{rslt[0][1]}</strong> by <strong>{rslt[0][3]}</strong>? If not, add some specific word to the song name")
                    return redirect('/suggestions')
                cur.execute("INSERT INTO suggestions (uid, song_name, name_std, song_author, likes) VALUES (?,?,?, ?, ?)", (uid, name,name_std, author, 0))
                conn.commit()
                succ_mess += "was added to the suggestion list"
                success.append(succ_mess)
            except sqlite3.Error as er:
                errors.append("There was a problem with writing into the database - check if the name and the author are not similar to some of the already listed suggestions")
                errors.append('SQLite error:' + ' '.join(er.args))

    return redirect('suggestions')

@app.route("/error")
def error():
    global errors
    if errors:
        nowerrors = errors.copy()
        errors = []

        return render_template("error.html", errors=nowerrors)
    return redirect("home")

def sec_to_mins_sec(sec: int):
    return f'{int(sec)//60}:{int(sec)%60}'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_name(name):
    '''
        Checks for html tags etc, should be improved
    '''
    return re.sub(r'<[^>]*?>','', ' '.join(filter(lambda x: len(x) > 0, name.strip().split())))

def opendb(db):
    '''
        Returns None when a corrupted or not found database, otherwise return a list - connection and cursor respectively
    '''
    if not os.path.isfile(db):
        errors.append('ERROR: .db does not exist')
        return None
    try:
        conn = sqlite3.connect(db)
    except sqlite3.Error :
        errors.append('ERROR: .db file not found or corrupted')
        return None
    cur = conn.cursor()
    return [conn, cur]

def get_song_duration(path):
    '''
        Returns None if path does not exist or problem with loading the file otherwise returns rounded duration in seconds
    '''
    try:
        audio = MP3(path)
        length = audio.info.length
        return round(length)
    except:
        return None

def get_song(id):
    cur_ret = opendb(DATABASE_PATH)
    if cur_ret is None:
        return None
    else:
        conn, cur = cur_ret
        conn.row_factory = sqlite3.Row

    res = cur.execute("SELECT id, song_name, song_author, song_img_path, song_duration_secs FROM songs WHERE id=? ", (id,))

    song = []
    for row in  cur.fetchall():
        col_names = [tup[0] for tup in res.description]
        row_val = [i for i in row]
        song.append(dict(zip(col_names,row_val)))
        
    return song

def get_songs():
    """ Returns a dictionary of songs from the database where a key 
        is the song_id and the value is a dictionary with additional info """

    #connection to an sqlite database
    cur_ret = opendb(DATABASE_PATH)

    if cur_ret is None:
        errors.append("Failed to connect to the database")
        return None
    else:
        conn, cur = cur_ret
        conn.row_factory = sqlite3.Row
    
    liked = [i[0] for i in cur.execute("SELECT song_id FROM likes_songs WHERE uid=?", (session.get('id', -1),)).fetchall()]
    res = cur.execute("SELECT * FROM songs")
    songs = {}
    for row in  cur.fetchall():
        col_names = [tup[0] for tup in res.description]
        row_val = [i for i in row]
        songs[row_val[0]] = dict(zip(col_names[1:],row_val[1:]))
        if session.get('id') is None:
            songs[row_val[0]]['liked'] = 0
        else:
            if row_val[0] in liked:
                songs[row_val[0]]['liked'] = 1
            else:
                songs[row_val[0]]['liked'] = 0

    return songs


def get_suggestions(uid=None):
    '''
        Return a list of dictionaries of suggestions with following keys:
            - id
            - user name ('uname') string
            - song name ('song_name') string
            - song_author ('song_author') string
            - liked ('liked') 0/1 whether the user liked that suggestion
        Otherwise returns None when problem with loading the database
    '''
    cur_ret = opendb(DATABASE_PATH)

    if cur_ret is None:
        return None
    else:
        conn, cur = cur_ret
        conn.row_factory = sqlite3.Row

    liked = [i[0] for i in cur.execute("SELECT sugg_id FROM likes_sugg WHERE uid=?", (session.get('id', -1),)).fetchall()] #list of the liked suggestion by the user

    if uid != None:
        res = cur.execute("SELECT suggestions.id, uname, song_name, song_author, likes FROM suggestions JOIN users ON suggestions.uid = users.id WHERE uid=? ", (uid,))
    else:
        res = cur.execute("SELECT suggestions.id, uname, song_name, song_author, likes FROM suggestions JOIN users ON suggestions.uid = users.id ")

    suggestions = []
    for row in  cur.fetchall():
        col_names = [tup[0] for tup in res.description]
        row_val = [i for i in row]
        suggestions.append(dict(zip(col_names,row_val)))
        if session.get('id') is None:
            suggestions[-1]['liked'] = 0
        else:
            if row_val[0] in liked:
                suggestions[-1]['liked'] = 1
            else:
                suggestions[-1]['liked'] = 0

    return suggestions

def check_if_in_database(song_name, song_author, id=None):
    '''
        Checks if a song by a certain author is already in the database,
         returns None if corrupted database, otherwise True when in databse, False when not
    '''
    cur_ret = opendb(DATABASE_PATH)

    if cur_ret is None:
        errors.append("Failed to connect to the database")
        return None
    else:
        conn, cur = cur_ret
        conn.row_factory = sqlite3.Row
    if id is None:
        cur.execute("SELECT * FROM songs WHERE song_name=? AND song_author=?", (song_name, song_author))
    else:
        cur.execute("SELECT * FROM songs WHERE song_name=? AND song_author=? AND id!=?", (song_name, song_author,id))
    if cur.rowcount > 0:
        return True
    return False

def rplc_spcl_char(stri):
    '''
        Replace specilal characters from slovak keyboard
    '''
    rpl = {
            "ľ":"l",
            "š": "s",
            "č": "c",
            "ť": "t",
            "ž": "z",
            "ý": "y",
            "á": "a",
            "í": "i",
            "é": "e",
            "ú": "u",
            "ä": "a",
            "ô": "o",
            "ň": "n",
            "ď": "d",
            "ó": "o",
         }
    stri = stri.lower().strip()
    new = ''

    for chr in stri:
        if chr == ' ' and new and new[-1] == ' ':
            continue
        if chr not in '`!\"£$%^&*()_+~}{-=#][\'\\;/.,<>?@:¬:':   
                new += rpl.get(chr, chr)
    
    return new


if __name__ == "__main__":

    songs_sq_mp3 = []
    cur_ret = opendb(DATABASE_PATH)
    sdict = {}
    if cur_ret is None:
        errors.append("Failed to connect to the database")
        exit
    else:
        print("Database opened succesfully")
        conn, cur = cur_ret
        cur.execute("SELECT id,song_mp3_path, song_txt_path, song_name, song_duration_secs FROM songs")
        song_list = list(cur.fetchall())
        for i in song_list:
            sdict[i[0]] = i
    manager = multiprocessing.Manager()
    d = manager.dict()

    if sdict:
	    d['currsong'] = min(sdict.keys())
    else:
	    d['currsong'] = 1
        
    d['currsecs'] = 0
    d['songs'] = sdict
    print(d)
    p1 = multiprocessing.Process(target = play_songs.playsong, args=(d,))
    p1.start()
    # p1.join()
    app.run(debug=False, host="0.0.0.0")
