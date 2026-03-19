from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_pace(time_minutes, distance_km):
    if distance_km == 0:
        return 0, "0:00 min/km"
    pace_min = time_minutes / distance_km
    pace_min_int = int(pace_min)
    pace_sec = int(round((pace_min - pace_min_int) * 60))
    pace_str = f"{pace_min_int}:{pace_sec:02d} min/km"
    return pace_min, pace_str

def calculate_speed(distance_km, time_minutes):
    if time_minutes == 0:
        return 0
    return round((distance_km / time_minutes) * 60, 2)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    show_result = False
    if request.method == 'POST':
        show_result = True
        try:
            distance = float(request.form['distance'])
            unit = request.form.get('unit', 'km')
            input_mode = request.form.get('input_mode', 'time')
            dist_km = distance if unit == 'km' else distance * 1.60934
            if input_mode == 'pace':
                pace_min = int(request.form.get('pace_min') or 0)
                pace_sec = int(request.form.get('pace_sec') or 0)
                pace = pace_min + pace_sec / 60
                total_minutes = pace * distance
                # Calculate time_h, time_m, time_s for display
                total_seconds = int(total_minutes * 60)
                time_h = total_seconds // 3600
                time_m = (total_seconds % 3600) // 60
                time_s = total_seconds % 60
                time_str = f"{time_h:02d}:{time_m:02d}:{time_s:02d}"
                pace_str = f"{pace_min}:{pace_sec:02d} min/{unit}"
                speed = calculate_speed(dist_km, total_minutes)
                speed_disp = round(speed if unit == 'km' else speed / 1.60934, 2)
            else:
                time_h = int(request.form.get('time_h') or 0)
                time_m = int(request.form.get('time_m') or 0)
                time_s = int(request.form.get('time_s') or 0)
                total_minutes = time_h * 60 + time_m + time_s / 60
                time_str = f"{time_h:02d}:{time_m:02d}:{time_s:02d}"
                pace, _ = calculate_pace(total_minutes, dist_km)
                pace_min_int = int(pace)
                pace_sec = int(round((pace - pace_min_int) * 60))
                pace_str = f"{pace_min_int}:{pace_sec:02d} min/{unit}"
                speed = calculate_speed(dist_km, total_minutes)
                speed_disp = round(speed if unit == 'km' else speed / 1.60934, 2)
            result = {
                'distance': distance,
                'unit': unit,
                'time_str': time_str,
                'pace': round(pace, 2) if input_mode == 'time' else pace,
                'pace_str': pace_str,
                'speed': speed_disp
            }
        except Exception as e:
            result = {'error': str(e)}
    return render_template('index.html', result=result, show_result=show_result)


@app.route('/health')
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
