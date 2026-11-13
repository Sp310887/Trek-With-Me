from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import mysql.connector
from mysql.connector import Error
import hashlib
import os
from datetime import datetime
import json
import re
import webbrowser
from threading import Timer

app = Flask(__name__)
app.secret_key = 'trekwithme_secret_key_2024'

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'trek_with_me',
    'user': 'root',
    'password': ''  # Change to your MySQL password
}

TREK_EXTRA_DETAILS = {
    'Roopkund Lake Trek': {
        'route_overview': 'The trek begins from Wan village and climbs through dense forests, meadows and rocky ridges before reaching the mysterious glacial lake at Roopkund.',
        'highlights': [
            'Snow-fed alpine meadows of Bedni and Ali Bugyal',
            'A uniquely eerie glacial lake surrounded by Himalayan peaks',
            'Stunning sunrise views over 5000m summits'
        ],
        'visit_spots': [
            'Bedni Bugyal',
            'Ali Bugyal',
            'Roopkund Lake',
            'Junargali ridge viewpoints'
        ],
        'activities': [
            'Camping under the stars',
            'Nature photography',
            'Guided acclimatization walks'
        ],
        'about_place': 'Roopkund is a high-altitude Himalayan trek in Uttarakhand with diverse terrain, from forest trails and wide meadows to a dramatic rocky lake basin at over 5000 meters.',
        'safety_tips': [
            'Acclimatize slowly and drink plenty of water.',
            'Listen to your guide and stay with the group.',
            'Carry warm layers; nights get very cold near the lake.'
        ],
        'donts': [
            'Do not hike alone or rush the ascent.',
            'Do not ignore altitude symptoms like headache or nausea.',
            'Do not leave the marked trail or litter the environment.'
        ],
    },
    'Valley of Flowers': {
        'route_overview': 'This trek follows a gentle trail through forests and meadows into a UNESCO heritage valley filled with flowers and alpine beauty.',
        'highlights': [
            'Endless fields of wild alpine flowers',
            'Crystal-clear streams and waterfalls',
            'Rich biodiversity and birdlife'
        ],
        'visit_spots': [
            'Valley of Flowers',
            'Hemkund Sahib glacial lake (optional)',
            'Bhujkhola and Khulara campsites'
        ],
        'activities': [
            'Floral photography',
            'Bird watching',
            'Peaceful meadow walks'
        ],
        'about_place': 'The Valley of Flowers in Chamoli, Uttarakhand is famous for its vibrant wildflowers, serene streams and dramatic mountain backdrop.',
        'safety_tips': [
            'Respect the fragile flora and keep to marked paths.',
            'Carry sunscreen and rain protection for changing weather.',
            'Stay hydrated during the trek.'
        ],
        'donts': [
            'Do not pick flowers or damage plant life.',
            'Do not stray from the trail.',
            'Do not make loud noises that disturb wildlife.'
        ],
    },
    'Kedarkantha Summit': {
        'route_overview': 'The trek starts from Sankri village, climbs through pine forests, and continues to open meadows before reaching the snowy Kedarkantha summit.',
        'highlights': [
            'Sunrise from the summit over the Himalayan range',
            'Snowy landscapes and panoramic ridge views',
            'Peaceful forest trails and high-altitude camps'
        ],
        'visit_spots': [
            'Sankri village',
            'Mane village',
            'Kedarkantha summit and ridge'
        ],
        'activities': [
            'Summit sunrise hike',
            'Snow trekking in winter',
            'Campfire evenings'
        ],
        'about_place': 'Kedarkantha is a popular Uttarakhand trek known for its accessible summit views, winter snow fields, and classic Himalayan scenery.',
        'safety_tips': [
            'Keep your boots dry and use proper winter gear in snow.',
            'Take rest breaks and monitor energy levels.',
            'Follow the guide on exposed sections near the summit.'
        ],
        'donts': [
            'Do not underestimate snow and low temperatures.',
            'Do not go ahead of the group on steep terrain.',
            'Do not ignore wet or icy trail conditions.'
        ],
    },
    'Hampta Pass Crossing': {
        'route_overview': 'The route crosses from lush Kullu valley to the stark Lahaul landscape, climbing through meadows, rocky slopes and finally across the pass.',
        'highlights': [
            'Dramatic contrast between green forests and barren lands',
            'Beautiful meadows and mountain views',
            'The iconic Hampta Pass saddle'
        ],
        'visit_spots': [
            'Jobra campsite',
            'Chikka campsite',
            'Hampta Pass',
            'Balu ka Ghera valley'
        ],
        'activities': [
            'Pass crossing adventure',
            'Photography of shifting landscapes',
            'Camp nights under the stars'
        ],
        'about_place': 'Hampta Pass in Himachal Pradesh is a classic trek that showcases two contrasting mountain environments in one itinerary.',
        'safety_tips': [
            'Be ready for rapid weather changes at the pass.',
            'Wear sturdy boots for loose and rocky sections.',
            'Carry rain protection; afternoon showers are common.'
        ],
        'donts': [
            'Do not try the pass in bad weather.',
            'Do not leave your group when crossing exposed areas.',
            'Do not discard waste in the mountains.'
        ],
    },
    'Chadar Frozen River Trek': {
        'route_overview': 'This extreme winter trek follows the frozen Zanskar River, with walking on ice, canyon walls and cold desert landscapes.',
        'highlights': [
            'Walking on a frozen river under towering cliffs',
            'The stark winter beauty of Ladakh',
            'Unique ice formations and frozen waterfalls'
        ],
        'visit_spots': [
            'Chadar River trail',
            'Nimu village start point',
            'Camping spots on ice'
        ],
        'activities': [
            'Ice hiking',
            'Winter photography',
            'Experiencing Ladakh’s cold desert culture'
        ],
        'about_place': 'Chadar is one of the most surreal winter treks in Ladakh, offering an unforgettable journey on the frozen Zanskar River.',
        'safety_tips': [
            'This trek requires proper winter equipment and experienced guidance.',
            'Keep your extremities warm and change wet socks immediately.',
            'Listen carefully to the guide on ice conditions.'
        ],
        'donts': [
            'Do not travel without specialist winter gear.',
            'Do not attempt ice walking alone.',
            'Do not ignore signs of frostbite or severe cold.'
        ],
    },
    'Triund Ridge Trek': {
        'route_overview': 'A short, scenic trek from Dharamshala up to the Triund ridge, crossing forests and ending at a rocky crest with valley views.',
        'highlights': [
            'Panoramic views of Kangra valley and Dhauladhar',
            'Beautiful rhododendron and oak forests',
            'A relaxed ridge-top camp experience'
        ],
        'visit_spots': [
            'Triund ridge',
            'Laka Glacier viewpoint',
            'Dharamkot village'
        ],
        'activities': [
            'Short hikes to viewpoints',
            'Camping with valley views',
            'Bird watching'
        ],
        'about_place': 'Triund is a popular easy trek near Dharamshala, ideal for quick mountain escapes with spectacular views and gentle trails.',
        'safety_tips': [
            'Carry enough water for the short ascent.',
            'Wear comfortable shoes for rocky sections.',
            'Start early to avoid afternoon heat on sunny days.'
        ],
        'donts': [
            'Do not leave trash on the ridge.',
            'Do not stray from the main trail.',
            'Do not underestimate the return descent.'
        ],
    },
    'Sandakphu Peak Trek': {
        'route_overview': 'The trek climbs through forests, rhododendron slopes and high-altitude villages before reaching the highest point in West Bengal.',
        'highlights': [
            'Rare views of four of the five highest peaks in the world',
            'Rhododendron forests and alpine yak pastures',
            'Rewarding sunrise from Sandakphu peak'
        ],
        'visit_spots': [
            'Sandakphu peak',
            'Phalut viewpoint',
            'Ravangla and Kalipokhri'
        ],
        'activities': [
            'High-altitude trekking',
            'Photography of Himalayan giants',
            'Village sightseeing'
        ],
        'about_place': 'Sandakphu offers one of the most iconic Himalayan panoramas, blending Darjeeling hill station charm with alpine trekking.',
        'safety_tips': [
            'Watch for altitude changes and carry warm clothing.',
            'Stay with the guide on narrow ridge sections.',
            'Drink enough water to stay hydrated.'
        ],
        'donts': [
            'Do not rush the climb at high altitude.',
            'Do not play with fire near dry grassland.',
            'Do not ignore mountain weather forecasts.'
        ],
    },
    'Chopta Tungnath Trek': {
        'route_overview': 'A short, beautiful trek from Chopta to the Tungnath temple and Chandrashila peak through meadows and pine forests.',
        'highlights': [
            'The highest Shiva temple in the world',
            'Panoramic Himalayan views from Chandrashila',
            'Lush alpine meadows and forests'
        ],
        'visit_spots': [
            'Chopta base',
            'Tungnath temple',
            'Chandrashila summit'
        ],
        'activities': [
            'Temple visit and sunrise hike',
            'Photography from Chandrashila',
            'Exploring forests and meadows'
        ],
        'about_place': 'Chopta Tungnath is a popular easy trek in Uttarakhand known for its spiritual temple destination and sweeping Himalayan panoramas.',
        'safety_tips': [
            'Wear good hiking shoes for rocky paths.',
            'Carry warm clothes for early mornings.',
            'Respect local customs at the temple.'
        ],
        'donts': [
            'Do not litter near the temple or trails.',
            'Do not disturb wildlife or livestock.',
            'Do not take shortcuts through fragile meadows.'
        ]
    }
}

DEFAULT_TREK_DETAILS = {
    'route_overview': 'This trek follows a scenic trail with varied terrain and local highlights, guided by experienced staff.',
    'highlights': ['Beautiful mountain views', 'Nature-rich trails', 'A memorable outdoor experience'],
    'visit_spots': ['Trail highlights and viewpoint stops', 'Local villages or camps', 'Scenic rest areas'],
    'activities': ['Guided hiking', 'Photography', 'Campfire evenings'],
    'about_place': 'This destination is known for its natural beauty, cultural atmosphere and rewarding trekking experience.',
    'safety_tips': ['Follow the guide at all times.', 'Carry water and stay hydrated.', 'Use proper trekking footwear.'],
    'donts': ['Do not leave the marked trail.', 'Do not litter.', 'Do not hike alone.'],
    'inclusions': [
        'Professional trekking guide and support staff',
        'Trek permit and campsite fees',
        'Basic meals during the trek',
        'Emergency medical kit and first-aid support'
    ],
    'exclusions': [
        'Personal hiking gear and sleeping bag',
        'Travel to and from the trek start point',
        'Personal insurance and rescue costs',
        'Any extra snacks or drinks not included in meals'
    ],
    'itinerary': [
        'Day 1: Arrive at base camp, settle in, and prepare for the trek ahead.',
        'Day 2: Follow scenic trails through forests, meadows, and viewpoint stops.',
        'Day 3: Reach the destination, enjoy the views, and return to the trailhead.'
    ]
}

def get_trek_extra_details(name):
    return TREK_EXTRA_DETAILS.get(name, DEFAULT_TREK_DETAILS)


def get_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"DB Error: {e}")
        return None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

EMAIL_PATTERN = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')

def is_valid_email(email):
    return bool(email) and EMAIL_PATTERN.match(email)

def is_valid_password(password):
    return bool(password) and len(password) >= 6

# ────────────────────────────────────────────────
# HOME
# ────────────────────────────────────────────────
@app.route('/')
def home():
    db = get_db()
    treks = []
    if db:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM treks WHERE is_active=1 ORDER BY rating DESC LIMIT 6")
        treks = cursor.fetchall()
        db.close()
    return render_template('index.html', treks=treks, user=session.get('user'))

# ────────────────────────────────────────────────
# AUTH
# ────────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        raw_password = request.form.get('password', '')
        phone = request.form.get('phone', '').strip()
        otp_verified = request.form.get('otp_verified', '0') == '1'

        if not name:
            flash('Please enter your full name.', 'error')
            return render_template('register.html')
        if not is_valid_email(email):
            flash('Enter a valid email address.', 'error')
            return render_template('register.html')
        if not is_valid_password(raw_password):
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html')
        if not phone:
            flash('Please enter your phone number.', 'error')
            return render_template('register.html')
        if not otp_verified:
            flash('Please verify your mobile OTP before creating your account.', 'error')
            return render_template('register.html')

        password = hash_password(raw_password)
        db = get_db()
        if db:
            cursor = db.cursor()
            try:
                cursor.execute(
                    "INSERT INTO users (name, email, password, phone) VALUES (%s,%s,%s,%s)",
                    (name, email, password, phone)
                )
                db.commit()
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            except Error as e:
                flash('Email already exists!', 'error')
            finally:
                db.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        raw_password = request.form.get('password', '')

        if not is_valid_email(email):
            flash('Enter a valid email address.', 'error')
            return render_template('login.html')
        if not raw_password:
            flash('Please enter your password.', 'error')
            return render_template('login.html')

        password = hash_password(raw_password)
        db = get_db()
        if db:
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
            user = cursor.fetchone()
            db.close()
            if user:
                session['user'] = {'id': user['id'], 'name': user['name'], 'email': user['email'], 'role': user.get('role','user')}
                if user.get('role') == 'admin':
                    return redirect(url_for('admin_dashboard'))
                return redirect(url_for('home'))
            else:
                flash('Invalid credentials!', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# ────────────────────────────────────────────────
# TREK LISTING
# ────────────────────────────────────────────────
@app.route('/treks')
def treks():
    db = get_db()
    trek_list = []
    if db:
        cursor = db.cursor(dictionary=True)
        difficulty = request.args.get('difficulty','')
        search = request.args.get('search','')
        query = "SELECT * FROM treks WHERE is_active=1"
        params = []
        if difficulty:
            query += " AND difficulty=%s"
            params.append(difficulty)
        if search:
            query += " AND (name LIKE %s OR location LIKE %s)"
            params.extend([f'%{search}%', f'%{search}%'])
        cursor.execute(query, params)
        trek_list = cursor.fetchall()
        db.close()
    return render_template('treks.html', treks=trek_list, user=session.get('user'))

@app.route('/trek/<int:trek_id>')
def trek_detail(trek_id):
    db = get_db()
    trek = None
    homestays = []
    pack_info = {}
    if db:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM treks WHERE id=%s", (trek_id,))
        trek = cursor.fetchone()
        cursor.execute("SELECT * FROM homestays WHERE trek_id=%s AND is_active=1", (trek_id,))
        homestays = cursor.fetchall()
        db.close()
    trek_details = DEFAULT_TREK_DETAILS
    if trek:
        difficulty = trek.get('difficulty', 'Moderate')
        duration_days = trek.get('duration_days') or 1
        base_weight = 6 if duration_days <= 3 else 9 if duration_days <= 6 else 12
        extra_weight = 2 if difficulty in ['Hard', 'Expert'] else 0
        min_weight = base_weight + extra_weight
        max_weight = min_weight + 3
        pack_items = [
            'Waterproof trekking backpack (35-45L)',
            'Layered clothing (base, mid, warm outer)',
            'Sturdy hiking boots with good ankle support',
            'Lightweight rain jacket and quick-dry layers',
            'Thermal socks, hat, gloves, and sun protection',
            'First-aid kit, headlamp, and personal medications',
            'Water bottle or hydration bladder',
            'Trekking poles and a compact sleeping bag'
        ]
        if difficulty in ['Hard', 'Expert']:
            pack_items.append('Extra insulation and backup warm layers')
        if duration_days > 5:
            pack_items.append('Portable stove or fuel for longer stays')
        food_plan = [
            {'meal': 'Breakfast', 'plan': 'Oatmeal, energy bars, dry fruits, tea or coffee.'},
            {'meal': 'Lunch', 'plan': 'High-protein wraps, nuts, sandwiches, and fresh fruit.'},
            {'meal': 'Snacks', 'plan': 'Trail mix, energy gels, chocolate, and electrolyte tablets.'},
            {'meal': 'Dinner', 'plan': 'Soups, rice/noodles, dehydrated meals, and warm drinks.'}
        ]
        if duration_days >= 7:
            food_plan.append({'meal': 'Extra', 'plan': 'Carry a small reserve of lightweight emergency rations.'})
        pack_info = {
            'weight_recommendation': f'Pack around {min_weight}-{max_weight} kg of essentials for this trek.',
            'weight_note': 'Keep your load balanced: prioritize hydration, shelter, and emergency gear first.',
            'pack_items': pack_items,
            'food_plan': food_plan,
            'hydration_tip': 'Drink regularly; aim for 2-3 liters a day depending on altitude and effort.'
        }
        trek_details = get_trek_extra_details(trek.get('name'))
        if 'itinerary' not in trek_details:
            itinerary = []
            for day in range(1, duration_days + 1):
                if day == 1:
                    itinerary.append(f'Day {day}: Reach base camp, gear check, and settle in for the first night.')
                elif day == duration_days:
                    itinerary.append(f'Day {day}: Complete the final stretch, reach the destination, and return to the trailhead.')
                else:
                    itinerary.append(f'Day {day}: Trek through scenic trails, campsites and viewpoints with guided support.')
            trek_details['itinerary'] = itinerary
    return render_template('trek_detail.html', trek=trek, homestays=homestays, pack_info=pack_info, trek_details=trek_details, user=session.get('user'))

# ────────────────────────────────────────────────
# BOOKING
# ────────────────────────────────────────────────
@app.route('/book/<int:trek_id>', methods=['GET', 'POST'])
def book(trek_id):
    if not session.get('user'):
        return redirect(url_for('login'))
    db = get_db()
    trek = None
    homestays = []
    if db:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM treks WHERE id=%s", (trek_id,))
        trek = cursor.fetchone()
        cursor.execute("SELECT * FROM homestays WHERE trek_id=%s AND is_active=1", (trek_id,))
        homestays = cursor.fetchall()
        db.close()
    if not trek:
        return redirect(url_for('treks'))

    initial_people = request.args.get('people', 1)
    try:
        initial_people = int(initial_people)
    except (TypeError, ValueError):
        initial_people = 1
    initial_people = min(max(initial_people, 1), 10)

    if request.method == 'POST':
        trek_date = request.form.get('trek_date', '').strip()
        try:
            num_people = int(request.form.get('num_people', 1))
        except (TypeError, ValueError):
            num_people = 1
        num_people = min(max(num_people, 1), 10)

        if not trek_date:
            flash('Please select a trek date.', 'error')
            return render_template('booking.html', trek=trek, homestays=homestays, user=session.get('user'), now=datetime.now().date().isoformat(), initial_people=num_people)

        try:
            selected_date = datetime.strptime(trek_date, '%Y-%m-%d').date()
            if selected_date < datetime.now().date():
                flash('Please choose today or a future date.', 'error')
                return render_template('booking.html', trek=trek, homestays=homestays, user=session.get('user'), now=datetime.now().date().isoformat(), initial_people=num_people)
        except ValueError:
            flash('Please enter a valid trek date.', 'error')
            return render_template('booking.html', trek=trek, homestays=homestays, user=session.get('user'), now=datetime.now().date().isoformat(), initial_people=num_people)

        homestay_id = request.form.get('homestay_id') or None
        trek_price = float(trek['price']) if trek and trek.get('price') is not None else 0.0
        total = trek_price * num_people
        if homestay_id:
            db2 = get_db()
            if db2:
                c2 = db2.cursor(dictionary=True)
                c2.execute("SELECT price_per_night FROM homestays WHERE id=%s", (homestay_id,))
                h = c2.fetchone()
                if h and h.get('price_per_night') is not None:
                    total += float(h['price_per_night']) * num_people
                db2.close()
        session['pending_booking'] = {
            'trek_id': trek_id,
            'trek_date': trek_date,
            'num_people': num_people,
            'homestay_id': homestay_id,
            'total': total,
            'trek_name': trek['name']
        }
        return redirect(url_for('payment'))
    now = datetime.now().date().isoformat()
    return render_template('booking.html', trek=trek, homestays=homestays, user=session.get('user'), now=now, initial_people=initial_people)

# ────────────────────────────────────────────────
# PAYMENT
# ────────────────────────────────────────────────
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if not session.get('user'):
        return redirect(url_for('login'))
    booking = session.get('pending_booking')
    if not booking:
        return redirect(url_for('treks'))
    if request.method == 'POST':
        payment_method = request.form.get('payment_method', 'upi')
        payment_reference = request.form.get('payment_reference', '').strip() or 'DEMO_PAYMENT'
        if payment_method == 'card' and payment_reference == 'DEMO_PAYMENT':
            payment_reference = 'DEMO_CARD_TXN'
        db = get_db()
        if db:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO bookings (user_id, trek_id, trek_date, num_people, homestay_id, total_amount, payment_status, payment_method, payment_reference) VALUES (%s,%s,%s,%s,%s,%s,'paid',%s,%s)",
                (session['user']['id'], booking['trek_id'], booking['trek_date'], booking['num_people'], booking['homestay_id'], float(booking['total']), payment_method, payment_reference)
            )
            db.commit()
            db.close()
        session.pop('pending_booking', None)
        flash('Booking confirmed! Dummy payment recorded and your booking is saved.', 'success')
        return redirect(url_for('my_bookings'))
    if booking and booking.get('total') is not None:
        try:
            booking['total'] = float(booking['total'])
        except (ValueError, TypeError):
            booking['total'] = 0.0
    else:
        booking['total'] = 0.0
    return render_template('payment.html', booking=booking, user=session.get('user'))

@app.route('/my-bookings')
def my_bookings():
    if not session.get('user'):
        return redirect(url_for('login'))
    db = get_db()
    bookings = []
    if db:
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT b.*, t.name as trek_name, t.image_url, t.location, h.name as homestay_name
            FROM bookings b JOIN treks t ON b.trek_id=t.id
            LEFT JOIN homestays h ON b.homestay_id=h.id
            WHERE b.user_id=%s ORDER BY b.created_at DESC
        """, (session['user']['id'],))
        bookings = cursor.fetchall()
        db.close()
    return render_template('my_bookings.html', bookings=bookings, user=session.get('user'))

# ────────────────────────────────────────────────
# SOS
# ────────────────────────────────────────────────
@app.route('/sos', methods=['GET', 'POST'])
def sos():
    if request.method == 'POST':
        data = request.get_json()
        db = get_db()
        if db:
            cursor = db.cursor()
            landmark = data.get('landmark') if data.get('landmark') else None
            cursor.execute(
                "INSERT INTO sos_alerts (user_id, latitude, longitude, message, landmark) VALUES (%s,%s,%s,%s,%s)",
                (session.get('user', {}).get('id'), data.get('lat'), data.get('lng'), data.get('message','SOS Alert'), landmark)
            )
            db.commit()
            db.close()
        return jsonify({'status': 'sent', 'message': 'SOS alert sent to emergency contacts!'})

    last_sos = None
    if session.get('user'):
        db = get_db()
        if db:
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM sos_alerts WHERE user_id=%s ORDER BY created_at DESC LIMIT 1", (session['user']['id'],))
            last_sos = cursor.fetchone()
            db.close()
    return render_template('sos.html', user=session.get('user'), last_sos=last_sos)

# ────────────────────────────────────────────────
# CONTACT
# ────────────────────────────────────────────────
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        db = get_db()
        if db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO contacts (name, email, message) VALUES (%s,%s,%s)", (name, email, message))
            db.commit()
            db.close()
        flash('Message sent! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', user=session.get('user'))

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        rating = request.form['rating']
        feedback_msg = request.form['feedback']
        db = get_db()
        if db:
            try:
                cursor = db.cursor()
                cursor.execute(
                    "INSERT INTO feedback (`name`, `email`, `rating`, `feedback`) VALUES (%s,%s,%s,%s)",
                    (name, email, rating, feedback_msg)
                )
                db.commit()
                flash('Thank you for your feedback!', 'success')
            except Error as e:
                flash('Unable to send feedback right now. Please try again later.', 'danger')
                print(f"Feedback DB Error: {e}")
            finally:
                db.close()
        else:
            flash('Unable to connect to the database. Please try again later.', 'danger')
        return redirect(url_for('feedback'))
    return render_template('feedback.html', user=session.get('user'))

# ────────────────────────────────────────────────
# RECOMMENDATIONS API
# ────────────────────────────────────────────────
@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    difficulty = data.get('difficulty', '')
    max_price = data.get('max_price', 9999999)
    db = get_db()
    treks = []
    if db:
        cursor = db.cursor(dictionary=True)
        q = "SELECT * FROM treks WHERE is_active=1 AND price<=%s"
        params = [max_price]
        if difficulty:
            q += " AND difficulty=%s"
            params.append(difficulty)
        q += " ORDER BY rating DESC LIMIT 4"
        cursor.execute(q, params)
        treks = cursor.fetchall()
        db.close()
    return jsonify(treks)

# ────────────────────────────────────────────────
# ADMIN
# ────────────────────────────────────────────────
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('login'))
        if session['user'].get('role') != 'admin':
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated

@app.route('/admin_dashboard')
@app.route('/admin')
@admin_required
def admin_dashboard():
    db = get_db()
    stats = {'users': 0, 'treks': 0, 'bookings': 0, 'revenue': 0}
    treks = []
    bookings = []
    users = []
    contacts = []
    sos_alerts = []
    feedback = []
    monthly_reports = []
    trek_revenue = []
    revenue_analytics = {
        'filtered_revenue': 0,
        'filtered_bookings': 0,
        'filtered_monthly': [],
        'from_date': None,
        'to_date': None
    }
    if db:
        cursor = db.cursor(dictionary=True)
        
        # Basic stats
        cursor.execute("SELECT COUNT(*) as cnt FROM users WHERE role='user'")
        stats['users'] = cursor.fetchone()['cnt']
        cursor.execute("SELECT COUNT(*) as cnt FROM treks")
        stats['treks'] = cursor.fetchone()['cnt']
        cursor.execute("SELECT COUNT(*) as cnt FROM bookings")
        stats['bookings'] = cursor.fetchone()['cnt']
        cursor.execute("SELECT SUM(total_amount) as rev FROM bookings WHERE payment_status='paid'")
        r = cursor.fetchone()
        stats['revenue'] = r['rev'] or 0
        
        # Treks
        cursor.execute("SELECT * FROM treks ORDER BY id DESC")
        treks = cursor.fetchall()
        
        # Bookings with revenue info
        cursor.execute("""SELECT b.*, u.name as user_name, t.name as trek_name
            FROM bookings b JOIN users u ON b.user_id=u.id JOIN treks t ON b.trek_id=t.id
            ORDER BY b.created_at DESC LIMIT 50""")
        bookings = cursor.fetchall()
        
        # Monthly reports
        cursor.execute("SELECT DATE_FORMAT(created_at, '%%Y-%%m') AS month_label, COUNT(*) AS booking_count, SUM(num_people) AS total_people, SUM(total_amount) AS total_amount FROM bookings WHERE payment_status='paid' GROUP BY YEAR(created_at), MONTH(created_at) ORDER BY YEAR(created_at) DESC, MONTH(created_at) DESC LIMIT 12")
        monthly_reports = cursor.fetchall()
        
        # Trek-wise revenue
        cursor.execute("""SELECT t.name as trek_name, COUNT(b.id) as booking_count, 
            SUM(b.total_amount) as total_revenue, AVG(b.total_amount) as avg_booking
            FROM treks t LEFT JOIN bookings b ON t.id = b.trek_id AND b.payment_status='paid'
            GROUP BY t.id, t.name ORDER BY total_revenue DESC""")
        trek_revenue = cursor.fetchall()
        
        # Revenue analytics - handle date filtering
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        
        if from_date and to_date:
            # Filtered revenue
            cursor.execute("""SELECT SUM(total_amount) as filtered_revenue, COUNT(*) as filtered_bookings
                FROM bookings WHERE payment_status='paid' 
                AND DATE(created_at) BETWEEN %s AND %s""", (from_date, to_date))
            filtered_data = cursor.fetchone()
            revenue_analytics['filtered_revenue'] = filtered_data['filtered_revenue'] or 0
            revenue_analytics['filtered_bookings'] = filtered_data['filtered_bookings'] or 0
            revenue_analytics['from_date'] = from_date
            revenue_analytics['to_date'] = to_date
            
            # Filtered monthly breakdown
            cursor.execute("""SELECT DATE_FORMAT(created_at, '%%Y-%%m') AS month_label, 
                COUNT(*) AS booking_count, SUM(total_amount) AS total_amount 
                FROM bookings WHERE payment_status='paid' 
                AND DATE(created_at) BETWEEN %s AND %s
                GROUP BY YEAR(created_at), MONTH(created_at) 
                ORDER BY YEAR(created_at) DESC, MONTH(created_at) DESC""", (from_date, to_date))
            revenue_analytics['filtered_monthly'] = cursor.fetchall()
        else:
            revenue_analytics['filtered_revenue'] = stats['revenue']
            revenue_analytics['filtered_bookings'] = stats['bookings']
            revenue_analytics['filtered_monthly'] = monthly_reports
        
        # Users, contacts, sos, feedback
        cursor.execute("SELECT * FROM users ORDER BY id DESC")
        users = cursor.fetchall()
        cursor.execute("SELECT * FROM contacts ORDER BY id DESC")
        contacts = cursor.fetchall()
        cursor.execute("SELECT s.*, u.name as user_name FROM sos_alerts s LEFT JOIN users u ON s.user_id=u.id ORDER BY s.created_at DESC")
        sos_alerts = cursor.fetchall()
        cursor.execute("SELECT * FROM feedback ORDER BY id DESC")
        feedback = cursor.fetchall()
        db.close()
    return render_template(
        'admin.html',
        stats=stats,
        treks=treks,
        bookings=bookings,
        users=users,
        contacts=contacts,
        sos_alerts=sos_alerts,
        feedback=feedback,
        monthly_reports=monthly_reports,
        trek_revenue=trek_revenue,
        revenue_analytics=revenue_analytics,
        user=session.get('user'),
        show_nav=False
    )

@app.route('/admin/sos/rescue/<int:sos_id>')
@admin_required
def admin_rescue_sos(sos_id):
    db = get_db()
    if db:
        cursor = db.cursor()
        rescue_message = 'Your SOS alert has been marked rescued by the admin. Please follow the rescue team instructions and stay safe.'
        try:
            cursor.execute("UPDATE sos_alerts SET status='resolved', admin_message=%s WHERE id=%s", (rescue_message, sos_id))
        except Error:
            cursor.execute("UPDATE sos_alerts SET status='resolved' WHERE id=%s", (sos_id,))
        db.commit()
        db.close()
    flash('SOS alert marked rescued.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/trek/add', methods=['POST'])
@admin_required
def admin_add_trek():
    data = request.form
    db = get_db()
    if db:
        cursor = db.cursor()
        cursor.execute("""INSERT INTO treks (name, location, description, difficulty, duration_days, price, image_url, latitude, longitude, max_altitude, rating)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (data['name'], data['location'], data['description'], data['difficulty'],
             data['duration_days'], data['price'], data['image_url'],
             data.get('latitude',0), data.get('longitude',0),
             data.get('max_altitude',''), data.get('rating', 4.0)))
        db.commit()
        db.close()
    flash('Trek added!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/trek/delete/<int:tid>')
@admin_required
def admin_delete_trek(tid):
    db = get_db()
    if db:
        cursor = db.cursor()
        cursor.execute("UPDATE treks SET is_active=0 WHERE id=%s", (tid,))
        db.commit()
        db.close()
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    url = 'http://127.0.0.1:5000'
    Timer(1.0, lambda: webbrowser.open_new(url)).start()
    app.run(debug=True, use_reloader=False)
