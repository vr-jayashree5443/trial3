from flask import Flask, render_template, request, redirect, session, Response
from datetime import date
import cv2
import mediapipe as mp
import math
import pymysql.cursors
import pandas as pd

# Initialize a variable with 0 time
plank_time= '00:00:00'




app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8znxec]/'

camera = None
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

curls = 0
curling = False
previous_angle3 = 180
previous_angle4 = 180

pushups=0


def start_camera():
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)

def stop_camera():
    global camera
    if camera is not None:
        camera.release()
        camera = None

def calculate_angle(a, b, c):
    radians = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
    angle = math.degrees(radians)
    if angle < 0:
        angle += 360
    if angle > 180:
        angle = 360 - angle
    return angle

def update_curl_count(current_angle3, current_angle4):
    global curls, curling, previous_angle3, previous_angle4

    if (40 < current_angle3 < 50 and not curling) or (40 < current_angle4 < 50 and not curling):
        curls += 1
        curling = True

    if (150 < current_angle3 < 180 and curling) or (150 < current_angle4 < 180 and curling):
        curling = False

    previous_angle3 = current_angle3
    previous_angle4 = current_angle4

    return curls

def generate_frames():
    global curls
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while True:
            if camera is not None:
                success, image = camera.read()
                if not success:
                    continue

                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = pose.process(image_rgb)
                if results.pose_landmarks:
                    left_shoulder = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
                                     results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y)
                    right_shoulder = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
                                      results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y)
                    left_elbow = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].x,
                                  results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y)
                    right_elbow = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].x,
                                   results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y)
                    left_wrist = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x,
                                  results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y)
                    right_wrist = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x,
                                   results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y)

                    angle3 = calculate_angle(left_shoulder, left_elbow, left_wrist)
                    angle4 = calculate_angle(right_shoulder, right_elbow, right_wrist)

                    curls = update_curl_count(angle3, angle4)

                    cv2.putText(image, f'Curls: {curls}', (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                ret, buffer = cv2.imencode('.jpg', image)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                break

    stop_camera()
'''    
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='QWE098*123asd',
        db='users',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        username = userDetails['username']
        password = userDetails['password']

        # Create database connection
        db = get_db_connection()

        try:
            with db.cursor() as cur:
                # Execute query
                cur.execute("INSERT INTO users(username, password) VALUES(%s, %s)", (username, password))
                # Commit to DB
                db.commit()
        finally:
            # Close database connection
            db.close()

        return redirect('/login')

    return render_template('templates/register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE username = %s AND password = %s"
                cursor.execute(sql, (username, password))
                user = cursor.fetchone()

                if user:
                    session['loggedin'] = True
                    session['username'] = username
                    return redirect('/video')
                else:
                    return 'Incorrect username or password!'
        finally:
            connection.close()

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect('/')
'''
from flask import Flask, render_template, request, redirect, session
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='QWE098*123asd',
        db='users',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        username = userDetails['username']
        password = userDetails['password']

        # Create database connection
        db = get_db_connection()

        try:
            with db.cursor() as cur:
                # Execute query
                cur.execute("INSERT INTO users(username, password) VALUES(%s, %s)", (username, password))
                # Commit to DB
                db.commit()
        finally:
            # Close database connection
            db.close()

        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE username = %s AND password = %s"
                cursor.execute(sql, (username, password))
                user = cursor.fetchone()

                if user:
                    session['loggedin'] = True
                    session['username'] = username
                    return redirect('/video')
                else:
                    return 'Incorrect username or password!'
        finally:
            connection.close()
            
            return redirect('/page2')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect('/')

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/curl')
def curl():
    return render_template('curl.html')


@app.route('/video')
def video():
    if 'loggedin' in session:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace;boundary=frame')
    else:
        return redirect('/login')

@app.route('/start')
def start():
    if 'loggedin' in session:
        start_camera()
        return 'Camera started!'
    else:
        return redirect('/login')

@app.route('/stop')
def stop():
    if 'loggedin' in session:
        stop_camera()
        return 'Camera stopped!'
    else:
        return redirect('/login')

@app.route('/finish', methods=['GET'])
def finish_stream():
    db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'QWE098*123asd',
    'database': 'users',
    'cursorclass': pymysql.cursors.DictCursor
        }
    # Get today's date
    today = date.today().strftime('%Y-%m-%d')
    global pushups
    global plank_time
    # Connect to the database
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            # Check if the entry exists for today's date and the current user
            check_query = "SELECT * FROM users_activities WHERE date = %s AND username = %s"
            cursor.execute(check_query, (today, 'current_username'))
            existing_entry = cursor.fetchone()

            if existing_entry:
                # If entry exists, update the values
                update_query = "UPDATE users_activities SET curl_count = curl_count + %s, pushup_count = pushup_count + %s, planks_time = ADDTIME(plank_time, %s) WHERE date = %s AND username = %s"
                cursor.execute(update_query, (curls, pushups, plank_time, today, 'current_username'))
            else:
                # If entry does not exist, insert a new row
                insert_query = "INSERT INTO users_activities (username, date, curl_count, pushup_count, planks_time) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(insert_query, ('current_username', today, curls, pushups, plank_time))

        # Commit changes to the database
        connection.commit()
        

    finally:
        # Close the connection
        connection.close()

    return redirect('/page2')


if __name__ == '__main__':
    app.run(debug=True)
