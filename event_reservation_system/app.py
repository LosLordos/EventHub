from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import Database
from repositories import EventRepository, UserRepository, BookingRepository, VenueRepository
from services import BookingService
import json
import os

app = Flask(__name__)

# Load secret key
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)
app.secret_key = config['app']['secret_key']

# Repositories
event_repo = EventRepository()
user_repo = UserRepository()
booking_repo = BookingRepository()
venue_repo = VenueRepository()
booking_service = BookingService()

@app.route('/')
def index():
    events = event_repo.get_all_upcoming()
    return render_template('index.html', events=events)

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = event_repo.get_by_id(event_id)
    if not event:
        return "Event not found", 404
    return render_template('event_detail.html', event=event)

@app.route('/book/<int:event_id>', methods=['POST'])
def book_ticket(event_id):
    # Simplified booking flow: 1 ticket per click or from form
    user_id = session.get('user_id')
    if not user_id:
        flash('Please login to book tickets', 'warning')
        return redirect(url_for('login'))
    
    quantity = int(request.form.get('quantity', 1))
    
    try:
        booking_service.create_booking(user_id, [{'event_id': event_id, 'quantity': quantity}])
        flash('Booking successful!', 'success')
    except Exception as e:
        flash(f'Booking failed: {str(e)}', 'danger')
        
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        # Simply get user by email (Authentication bypass for demo simplicity as password check is not main focus, 
        # but in real app we check hash)
        user = user_repo.get_by_email(email)
        if user:
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['name'] = user['display_name']
            flash(f'Welcome {user["display_name"]}', 'success')
            return redirect(url_for('index'))
        else:
            flash('User not found', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out', 'info')
    return redirect(url_for('index'))

@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        return "Unauthorized", 403
    
    events = event_repo.get_all()
    venues = venue_repo.get_all()
    return render_template('admin.html', events=events, venues=venues)

@app.route('/admin/create_event', methods=['POST'])
def create_event():
    if session.get('role') != 'admin':
        return "Unauthorized", 403
        
    event_repo.create(
        venue_id=request.form['venue_id'],
        title=request.form['title'],
        description=request.form['description'],
        start_time=request.form['start_time'],
        base_price=float(request.form['base_price'])
    )
    flash("Event created", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/report')
def report():
    # Use the view v_revenue_report
    conn = Database().get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM v_revenue_report")
    report_data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('report.html', report=report_data)

@app.route('/admin/import', methods=['POST'])
def import_data():
    if session.get('role') != 'admin':
        return "Unauthorized", 403
    
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('admin_dashboard'))
        
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('admin_dashboard'))

    if file:
        try:
            content = file.read().decode('utf-8')
            from importer import DataImporter
            importer = DataImporter()
            results = importer.import_from_json(content)
            flash(f"Imported {results['events']} events and {results['users']} users. Errors: {len(results['errors'])}", "success")
        except Exception as e:
            flash(f"Import failed: {str(e)}", "danger")
            
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
