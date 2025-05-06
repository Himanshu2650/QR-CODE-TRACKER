# from flask import Flask, render_template, request, jsonify
# from datetime import datetime
# import os
# import csv
# from utils.pdf_generator import generate_pdf
# from utils.email_sender import send_email

# app = Flask(__name__)
# CSV_FILE = 'temp/data.csv'

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/start', methods=['POST'])
# def start_walk():
#     try:
#         os.makedirs('temp', exist_ok=True)
#         start_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

#         with open(CSV_FILE, 'w', newline='') as file:
#             writer = csv.writer(file)
#             # Write Start Time in the first row with headers
#             writer.writerow(['Start Time'])
#             # Add the actual start time in the second row
#             writer.writerow([start_time])

#         print("Start time saved:", start_time)
#         return jsonify({'status': 'started', 'start_time': start_time})
#     except Exception as e:
#         print("Error in /start:", e)
#         return jsonify({'status': 'error', 'message': str(e)}), 500

# @app.route('/scan', methods=['POST'])
# def scan_qr():
#     data = request.json
#     scan_time = data.get('scan_time')
#     gps = data.get('gps')
#     address = data.get('address')
#     qr_text = data.get('qr_text')

#     try:
#         # Append the scan data to the CSV file
#         with open(CSV_FILE, 'a', newline='') as f:
#             writer = csv.writer(f)
#             # Write the scan data in the next row
#             writer.writerow([scan_time, address])
#         return jsonify({'status': 'success'})
#     except Exception as e:
#         print("Error in /scan:", e)
#         return jsonify({'status': 'error', 'message': str(e)}), 500

# @app.route('/submit', methods=['POST'])
# def submit_walk():
#     try:
#         os.makedirs('temp', exist_ok=True)
#         Submit_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

#         with open(CSV_FILE, 'a', newline='') as file:
#             writer = csv.writer(file)
#             # Write Start Time in the first row with headers
#             writer.writerow(['Submit Time'])
#             # Add the actual start time in the second row
#             writer.writerow([Submit_time])

#         print("Start time saved:", Submit_time)
#         pdf_path = generate_pdf(CSV_FILE)
#         send_email(pdf_path)
#         os.remove(CSV_FILE)
#         os.remove(pdf_path)
#         return jsonify({'status': 'submitted', 'Submit_time': Submit_time})
#     except Exception as e:
#         print("Error in /submit:", e)
#         return jsonify({'status': 'error', 'message': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)

#-------------------------------------------------------------------------------------------
# from flask import Flask, render_template, request, jsonify
# from datetime import datetime
# import os
# import csv
# from utils.pdf_generator import generate_pdf
# from utils.email_sender import send_email

# app = Flask(__name__)
# today_date = datetime.now().strftime('%d-%m-%Y')
# CSV_FILE = f'temp/data_{today_date}.csv'

# pending_scans = {}
# checklist_data = {}

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/start', methods=['POST'])
# def start_walk():
#     try:
#         os.makedirs('temp', exist_ok=True)
#         start_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

#         with open(CSV_FILE, 'w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(['Start Time'])
#             writer.writerow([start_time])
#             writer.writerow([])
#             writer.writerow(['QR Code', 'Scan Time', 'GPS', 'Address', 'Checklist'])

#         pending_scans.clear()
#         checklist_data.clear()

#         return jsonify({'status': 'started', 'start_time': start_time})
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500

# @app.route('/scan', methods=['POST'])
# def scan_qr():
#     data = request.json
#     qr_text = data.get('qr_text')
#     scan_time = data.get('scan_time')
#     gps = data.get('gps')
#     address = data.get('address')

#     try:
#         pending_scans[qr_text] = {
#             'scan_time': scan_time,
#             'gps': gps,
#             'address': address
#         }
#         return jsonify({'status': 'success'})
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500

# @app.route('/submit-checklist', methods=['POST'])
# def submit_checklist():
#     data = request.json
#     qr_code = data.get('qr_code')
#     checklist_items = data.get('checklist')  # List of selected items

#     if not qr_code or not checklist_items:
#         return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

#     try:
#         scan_info = pending_scans.get(qr_code, {})
#         scan_time = scan_info.get('scan_time', '')
#         gps = scan_info.get('gps', '')
#         address = scan_info.get('address', '')

#         formatted_checklist = format_checklist_two_columns(checklist_items)

#         with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
#             writer = csv.writer(f)
#             writer.writerow([qr_code, scan_time, gps, address])
#             writer.writerow([f"Checklist for {qr_code}"])
#             writer.writerow([formatted_checklist])
#             writer.writerow([])

#         return jsonify({'status': 'success'})
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500

# @app.route('/submit', methods=['POST'])
# def submit_walk():
#     try:
#         submit_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
#         with open(CSV_FILE, 'a', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow([])
#             writer.writerow(['Submit Time'])
#             writer.writerow([submit_time])

#         pdf_path = generate_pdf(CSV_FILE)
#         send_email(pdf_path)

#         os.remove(pdf_path)
#         pending_scans.clear()
#         checklist_data.clear()

#         return jsonify({'status': 'submitted', 'submit_time': submit_time})
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500

# def format_checklist_two_columns(selected_items):
#     full_list = [
#         "Oil Leakage",
#         "Encroachment",
#         "Dumping of Rail Sleepers, M/Sand Metal etc.",
#         "Removal of trees/branches",
#         "Grass Cutting",
#         "Pipeline protection net, Door & lock",
#         "Fire Incident",
#         "Missing of Boundary pillars",
#         "Wastages/Plastic bins",
#         "Filling of earth hole",
#         "Replacement/Repairing of Signage boards",
#         "Checking of Cattles",
#         "TLP Box"
#     ]

#     lines = []
#     for i in range(0, len(full_list), 2):
#         left = full_list[i]
#         right = full_list[i + 1] if i + 1 < len(full_list) else ""

#         left_mark = "☑" if left in selected_items else "☐"
#         right_mark = "☑" if right in selected_items else "☐" if right else ""

#         left_text = f"{left_mark} {left}"
#         right_text = f"{right_mark} {right}" if right else ""

#         lines.append(f"{left_text:<45}{right_text}")
#     return "\n".join(lines)

# if __name__ == '__main__':
#     app.run(debug=True)


#----------------------------------------------------------------------------------

#------------------------------------NEW VERSION------------------------------------------
# from flask import Flask, render_template, request, jsonify
# from datetime import datetime
# import os
# import csv
# from utils.pdf_generator import generate_pdf
# from utils.email_sender import send_email

# app = Flask(__name__)
# today_date = datetime.now().strftime('%d-%m-%Y')
# CSV_FILE = f'temp/data_{today_date}.csv'
# pending_scans = {}

# checklists_by_location = {
#     "BPCL Admin Building": [
#         ["Oil Leakage", "Encroachment"],
#         ["Fire Incident", "Missing of Boundary pillars"],
#         ["Wastages/Plastic bins", "Grass Cutting"],
#         ["Removal of trees/branches", "Filling of earth hole"],
#         ["Replacement/Repairing of Warning boards"],
#         ["Checking of Cattles", "TLP Box"]
#     ],
#     "BPCL Entry Gate": [
#         ["Oil Leakage", "Encroachment"],
#         ["Dumping of Rail Sleepers, M/Sand Metal etc."],
#         ["Removal of trees/branches", "Grass Cutting"],
#         ["Pipeline protection net, Door & lock"]
#     ],
#     "BPCL Admin Annex Building": [
#         ["Oil Leakage", "Encroachment"],
#         ["Removal of 03 X boundary pillars named 'SR' placed by the Railway"],
#         ["Visibility of boundary pillars", "Grass Cutting"],
#         ["Wastages/Plastic bins", "Missing of Boundary pillars"],
#         ["Cultivation of Banana trees/vegetables etc."],
#         ["Repair/replacement of warning boards", "TLP Box"],
#         ["Pipeline protection net, Door & lock at Canal Crossing No 1, Error"]
#     ],
#     "T p r Business plaza": [
#         ["Oil Leakage", "Encroachment"],
#         ["Dumping of house construction materials."],
#         ["Wastages/Plastic bins", "Fire Incident"],
#         ["TLP Box", "Repair / Replacement of Warning boards"],
#         ["Cultivation of Banana trees/vegetables etc."],
#         ["Removal of trees branches", "Missing of Boundary pillars"],
#         ["Pipeline protection net, Door & lock at Kaniyampuzha"],
#         ["Removal of concrete pipe dumped on the pipeline"]
#     ]
# }

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/start', methods=['POST'])
# def start_walk():
#     try:
#         os.makedirs('temp', exist_ok=True)
#         start_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

#         with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
#             writer = csv.writer(file)
#             writer.writerow(['Start Time'])
#             writer.writerow([start_time])
#             writer.writerow([])
#             writer.writerow(['Scan Time', 'Address', 'Checklist'])

#         pending_scans.clear()
#         return jsonify({'status': 'started', 'start_time': start_time})
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500

# @app.route('/scan', methods=['POST'])
# def scan_qr():
#     data = request.json
#     qr_text = data.get('qr_text')
#     scan_time = data.get('scan_time')
#     address = data.get('address')

#     try:
#         pending_scans[qr_text] = {
#             'scan_time': scan_time,
#             'address': address
#         }
#         checklist = checklists_by_location.get(qr_text, [[item] for row in checklists_by_location.values() for sublist in row for item in sublist])
#         return jsonify({'status': 'success', 'checklist': checklist})
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500

# @app.route('/submit-checklist', methods=['POST'])
# def submit_checklist():
#     data = request.json
#     qr_code = data.get('qr_code')
#     checklist_items = data.get('checklist')

#     if not qr_code or not checklist_items:
#         return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

#     try:
#         scan_info = pending_scans.get(qr_code, {})
#         scan_time = scan_info.get('scan_time', '')
#         address = scan_info.get('address', '')

#         layout = checklists_by_location.get(qr_code, [[item] for row in checklists_by_location.values() for sublist in row for item in sublist])
#         formatted_checklist = format_checklist_layout(layout, checklist_items)

#         with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
#             writer = csv.writer(f)
#             writer.writerow([scan_time, address])
#             writer.writerow([f"Checklist for {qr_code}"])
#             writer.writerow([formatted_checklist])
#             writer.writerow([])

#         return jsonify({'status': 'success'})
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500

# @app.route('/submit', methods=['POST'])
# def submit_walk():
#     try:
#         submit_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
#         with open(CSV_FILE, 'a', newline='', encoding='utf-8') as file:
#             writer = csv.writer(file)
#             writer.writerow([])
#             writer.writerow(['Submit Time'])
#             writer.writerow([submit_time])

#         pdf_path = generate_pdf(CSV_FILE)
#         if pdf_path:
#             send_email(pdf_path)
#             #os.remove(pdf_path)

#         pending_scans.clear()
#         return jsonify({'status': 'submitted', 'submit_time': submit_time})
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500

# def format_checklist_layout(layout, selected_items):
#     lines = []
#     for row in layout:
#         left = row[0] if len(row) > 0 else ''
#         right = row[1] if len(row) > 1 else ''

#         left_mark = "☑" if left in selected_items else "☐"
#         right_mark = "☑" if right in selected_items else "☐" if right else ""

#         left_text = f"{left_mark} {left}"
#         right_text = f"{right_mark} {right}" if right else ""

#         lines.append(f"{left_text:<35}{right_text}")
#     return "\n".join(lines)

# if __name__ == '__main__':
#     app.run(debug=True)

###------------------------GPS VERSION---------------------------------------------

from flask import Flask, render_template, request, jsonify
import csv
import os
import folium
from datetime import datetime
from geopy.geocoders import Nominatim 
from utils.pdf_generator import generate_checklist_pdf, generate_map_pdf

from utils.email_sender import send_email_with_attachments 

app = Flask(__name__)
geolocator = Nominatim(user_agent="walk_tracker")  # ✅ [Initialize geolocator]

DATA_FILE = 'temp/data.csv'
MAP_IMAGE = 'static/walk_map.png'
MAP_HTML = 'temp/map.html'
PDF_REPORT = 'temp/walk_report.pdf'
CSV_FILE = 'temp/Report.csv'
os.makedirs('temp', exist_ok=True)
os.makedirs('static', exist_ok=True)

pending_scans = {}

checklists_by_location = {
    "BPCL Admin Building": [
        ["Oil Leakage", "Encroachment"],
        ["Fire Incident", "Missing of Boundary pillars"],
        ["Wastages/Plastic bins", "Grass Cutting"],
        ["Removal of trees/branches", "Filling of earth hole"],
        ["Replacement/Repairing of Warning boards"],
        ["Checking of Cattles", "TLP Box"]
    ],
    "BPCL Entry Gate": [
        ["Oil Leakage", "Encroachment"],
        ["Dumping of Rail Sleepers, M/Sand Metal etc."],
        ["Removal of trees/branches", "Grass Cutting"],
        ["Pipeline protection net, Door & lock"]
    ],
    "BPCL Admin Annex Building": [
        ["Oil Leakage", "Encroachment"],
        ["Removal of 03 X boundary pillars named 'SR' placed by the Railway"],
        ["Visibility of boundary pillars", "Grass Cutting"],
        ["Wastages/Plastic bins", "Missing of Boundary pillars"],
        ["Cultivation of Banana trees/vegetables etc."],
        ["Repair/replacement of warning boards", "TLP Box"],
        ["Pipeline protection net, Door & lock at Canal Crossing No 1, Error"]
    ],
    "T p r Business plaza": [
        ["Oil Leakage", "Encroachment"],
        ["Dumping of house construction materials."],
        ["Wastages/Plastic bins", "Fire Incident"],
        ["TLP Box", "Repair / Replacement of Warning boards"],
        ["Cultivation of Banana trees/vegetables etc."],
        ["Removal of trees branches", "Missing of Boundary pillars"],
        ["Pipeline protection net, Door & lock at Kaniyampuzha"],
        ["Removal of concrete pipe dumped on the pipeline"]
    ]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_walk', methods=['POST'])
def start_walk():
    data = request.get_json()
    lat = data.get('lat')
    lon = data.get('lon')
    Timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    location = geolocator.reverse((lat, lon), language='en')  # ✅ [Reverse geocoding]
    address = location.address if location else 'N/A'

    # ✅ Updated to include Address column
    with open(DATA_FILE, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Timestamp', 'Latitude', 'Longitude', 'Address'])
        writer.writerow([Timestamp, lat, lon, address])

    return jsonify({
        "message": "✅ Walk started and first GPS point saved.",
        "start_time": Timestamp
    })

@app.route('/save_location', methods=['POST'])  # ✅ [New endpoint with address saving]
def save_location():
    data = request.get_json()
    lat = data['latitude']
    lon = data['longitude']
    Timestamp = data['Timestamp']
    location = geolocator.reverse((lat, lon), language='en')
    address = location.address if location else 'N/A'

    with open(DATA_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([Timestamp, lat, lon, address])

    return {'status': 'saved'}


@app.route('/scan', methods=['POST'])
def scan_qr():
    data = request.json
    qr_text = data.get('qr_text')

    try:
        # Just return checklist without saving scan time or address
        checklist = checklists_by_location.get(qr_text, [[item] for row in checklists_by_location.values() for sublist in row for item in sublist])
        return jsonify({'status': 'success', 'checklist': checklist})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/submit-checklist', methods=['POST'])
def submit_checklist():
    data = request.json
    qr_code = data.get('qr_code')
    checklist_items = data.get('checklist')

    if not qr_code or not checklist_items:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

    try:
        # Get checklist layout for the QR code
        layout = checklists_by_location.get(qr_code, [[item] for row in checklists_by_location.values() for sublist in row for item in sublist])

        # Filter out any invalid items
        formatted_checklist = format_checklist_layout(layout, checklist_items)

        # Write only checklist to the CSV
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([qr_code, formatted_checklist]) 

        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/submit_walk', methods=['POST'])
def submit_walk():
    if not os.path.exists(DATA_FILE):
        return "❌ No data file found."

    lats, lons, Timestamps = [], [], []

    with open(DATA_FILE, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                if not row['Latitude'] or not row['Longitude']:
                    continue
                lats.append(float(row['Latitude']))
                lons.append(float(row['Longitude']))
                Timestamps.append(row['Timestamp'])
            except (ValueError, KeyError):
                continue

    if not lats or not lons:
        return "❌ No GPS points captured."

    walk_map = folium.Map(location=[lats[0], lons[0]], zoom_start=17)
    coordinates = list(zip(lats, lons))
    folium.PolyLine(coordinates, color='blue', weight=5).add_to(walk_map)
    folium.Marker(coordinates[0], tooltip='Start', icon=folium.Icon(color='green')).add_to(walk_map)
    folium.Marker(coordinates[-1], tooltip='End', icon=folium.Icon(color='red')).add_to(walk_map)

    walk_map.save(MAP_HTML)

    # Convert HTML map to PNG using selenium
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(800, 600)
    driver.get(f'file://{os.path.abspath(MAP_HTML)}')
    driver.save_screenshot(MAP_IMAGE)
    driver.quit()
    
    CHECKLIST_PDF = 'temp/report.pdf'
    
    generate_checklist_pdf(CSV_FILE, CHECKLIST_PDF)
    generate_map_pdf(MAP_IMAGE, PDF_REPORT)


    try:
        send_email_with_attachments(PDF_REPORT, CHECKLIST_PDF)
        
    except Exception as e:
        return f"✅ Map created, ❌ Email failed: {str(e)}"

    open(DATA_FILE, 'w').close()
    if os.path.exists(CSV_FILE): os.remove(CSV_FILE)
    return "✅ Walk map created, emailed, and data cleared!"

def format_checklist_layout(layout, selected_items):
    lines = []
    for row in layout:
        left = row[0] if len(row) > 0 else ''
        right = row[1] if len(row) > 1 else ''

        left_mark = "☑" if left in selected_items else "☐"
        right_mark = "☑" if right in selected_items else "☐" if right else ""

        left_text = f"{left_mark} {left}"
        right_text = f"{right_mark} {right}" if right else ""

        lines.append(f"{left_text:<35}{right_text}")
    return "\n".join(lines)


if __name__ == '__main__':
    app.run(debug=True)

