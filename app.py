from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# --- DATABASE SIMULATION ---
# In a real app, this would be SQL. Here, we use a simple list for the demo.
# Let's create a bus with 20 seats (4 rows of 5 or similar)
# Status: 'available', 'booked'
bus_seats = {}
rows = 5
cols = ['A', 'B', 'C', 'D'] # 2 seats left, 2 seats right

# Initialize seats
for r in range(1, rows + 1):
    for c in cols:
        seat_id = f"{r}{c}"
        bus_seats[seat_id] = "available"

# Pre-book a few seats to make it look realistic
bus_seats['1A'] = 'booked'
bus_seats['2C'] = 'booked'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-seats', methods=['GET'])
def get_seats():
    return jsonify(bus_seats)

@app.route('/book-ticket', methods=['POST'])
def book_ticket():
    data = request.json
    seat_id = data.get('seat')
    name = data.get('name')
    route = data.get('route')
    
    if bus_seats.get(seat_id) == 'available':
        bus_seats[seat_id] = 'booked'
        
        # Generate a fake Ticket ID
        ticket_id = f"JMD-{random.randint(1000, 9999)}"
        
        return jsonify({
            'success': True,
            'ticket_id': ticket_id,
            'seat': seat_id,
            'passenger': name,
            'message': 'Booking Successful!'
        })
    else:
        return jsonify({'success': False, 'message': 'Seat already taken!'})

if __name__ == '__main__':
    app.run(debug=True)