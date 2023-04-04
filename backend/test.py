#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from werkzeug import datastructures
from datetime import date, datetime

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
					   port = 8889,
                       user='root',
                       password='root',
                       db='airspace',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

#Define route for login
@app.route('/customer_login')
def customer_login():
	return render_template('customer_login.html')

#Define route for login
@app.route('/airstaff_login')
def airstaff_login():
	return render_template('airstaff_login.html')

#Define route for register
@app.route('/customer_registration')
def customer_registration():
	return render_template('customer_registration.html')

#Define route for airline_registration
@app.route('/airstaff_registration')
def airstaff_register():
	return render_template('airstaff_registration.html')

#Define route for airline_registration
@app.route('/customer_home')
def customer_home():
	return render_template('customer_home.html')

#Define route for airline_registration
@app.route('/airstaff_home')
def airstaff_home():
	return render_template('airstaff_home.html')

#Define route for add_airport
@app.route('/add_airport')
def add_airport():
	return render_template('add_airport.html')

#Define route for add_airport
@app.route('/airstaff_ratings')
def airstaff_ratings():
	return render_template('airstaff_ratings.html')

#Define route for add_airplane
@app.route('/add_airplane')
def add_airplane():
	return render_template('add_airplane.html')

#Define route for add_flight
@app.route('/add_flight')
def add_flight():
	return render_template('add_flight.html')

#Define route for airstaff_change_status
@app.route('/airstaff_change_status')
def airstaff_change_status():
	return render_template('airstaff_change_status.html')

#Define route for customer_ratings_comments
@app.route('/customer_ratings_comments')
def customer_ratings_comments():
	return render_template('customer_ratings_comments.html')

#Define route for view_reports
@app.route('/view_reports')
def view_reports():
    return render_template('view_reports.html')

#Define route for public_info
@app.route('/public_info')
def public_info():
	return render_template('public_info.html')

#Define route for future_flights
@app.route('/customer_future_flights')
def customer_future_flights():
    return render_template('customer_future_flights.html')

#Define route for future_flights
@app.route('/airstaff_future_flights')
def airstaff_future_flights():
    return render_template('airstaff_future_flights.html')

#Define route for flight_status
@app.route('/flight_status')
def flight_status():
    return render_template('flight_status.html')

#Define route for purchase_ticket
@app.route('/purchase_ticket')
def purchase_ticket():
    return render_template('purchase_ticket.html')

#Define route for customer_viewflights : Nakeya Adams
@app.route('/customer_viewflights')
def customer_viewflights_route():
	return render_template('customer_viewflights.html')

#Define route for purchase ticket: Juliana Soranno
@app.route('/purchase_ticketAuth', methods=['GET', 'POST'] )
def purchase_ticketAuth():
	#things to fix: 
	#	make sure card isnt expired
	
	email = session['email']

	#flight information
	airline_name = request.form['airline_name']
	flight_number = request.form['flight_number']
	departure_timestamp = request.form['departure_timestamp']

	#Credit card information
	name_on_card = request.form['name_on_card']
	card_number = request.form['card_number']
	exp_date = request.form['exp_date']
	card_type = request.form['card_type']

	cursor = conn.cursor()
	query = ("SELECT * FROM flight WHERE airline_name = %s AND flight_number = %s AND departure_timestamp = %s " +
			"AND departure_timestamp >= %s")
	cursor.execute(query, (airline_name, flight_number, departure_timestamp, datetime.now()))
	flight = cursor.fetchone()

	error = None
	if(flight): # if the flight exists:
		#to caculate the ticket id
		num_tickets_query = "SELECT COUNT(ticket_id) as num_tickets FROM ticket"
		cursor.execute(num_tickets_query)
		num_tickets = cursor.fetchone()
		ticket_id = num_tickets['num_tickets'] + 1

		#to caculate the number of seats on the flights
		num_seats_query = ("SELECT num_seats from airplane, flight where airplane.airplane_id = flight.airplane_id " +
							"and airplane.airplane_id = %s")
		cursor.execute(num_seats_query , (flight['airplane_id']))
		num_seats = cursor.fetchone()

		#to caculate how many passengers already with a ticket
		passengers_query = ("SELECT COUNT(ticket_id) as num FROM ticket where flight_number = %s")
		cursor.execute(passengers_query, (flight['airplane_id']))
		num_passenger = cursor.fetchone()
		
		print(flight['base_price'])

		#if there are available seats on the plane
		if(num_passenger['num'] <= num_seats['num_seats']): 
			#if 75% is booked, increase the price by .25
			if num_passenger['num'] >= num_seats['num_seats'] * .75:
				new_price = int(flight['base_price']) + (int(flight['base_price']) * .25)
			else:
				new_price = flight['base_price']
		
			query2 = ("INSERT INTO ticket (ticket_id, airline_name, sold_price, card_number, name_on_card, exp_date, " +
											"card_type, purchase_timestamp, flight_number, departure_timestamp) " + 
					"VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s )")
			cursor.execute(query2, (ticket_id, airline_name, new_price, card_number, name_on_card, exp_date,
									card_type, datetime.now(), flight_number, departure_timestamp ))
			query3 = ("INSERT INTO purchased_by (ticket_id , email) VALUES (%s, %s)")
			cursor.execute(query3, (ticket_id, email))
			conn.commit()
			
			return render_template("purchase_ticket.html" )
		else:
			error = "Sorry! No avaiable seats at this time"
			return render_template("purchase_ticket.html" , error=error) 
	else:
		error = "Flight does not exist/ card information incorrect"
		return render_template("purchase_ticket.html" , error=error)

#Define route for top destination: Paul Kim
@app.route('/top_destinations')
def top_destinations():
    username = session['username']
    cursor = conn.cursor()
    query = ('SELECT airline_name FROM airline_staff WHERE username = %s')
    cursor.execute(query, (username))
    airline_name = cursor.fetchone()
    query = ("SELECT airport.air_city, COUNT(ticket.flight_number) as total From airport, flight, ticket WHERE airport.air_code = flight.arrival_code and ticket.flight_number = flight.flight_number and ticket.airline_name = %s and ticket.departure_timestamp < CURRENT_DATE and ticket.departure_timestamp >= date_sub(current_date, INTERVAL 3 MONTH) GROUP By ticket.flight_number ORDER BY total DESC LIMIT 3")
    cursor.execute(query, (airline_name['airline_name']))
    three_month = cursor.fetchall()
    query = ("SELECT airport.air_city, COUNT(ticket.flight_number) as total From airport, flight, ticket WHERE airport.air_code = flight.arrival_code and ticket.flight_number = flight.flight_number and ticket.airline_name = %s and ticket.departure_timestamp < CURRENT_DATE and ticket.departure_timestamp >= date_sub(current_date, INTERVAL 1 Year) GROUP By ticket.flight_number ORDER BY total DESC LIMIT 3")
    cursor.execute(query, (airline_name['airline_name']))
    last_year = cursor.fetchall()
    cursor.close()
    return render_template('top_destinations.html', three_month = three_month, last_year = last_year)

#Define route for airstaff_viewflights
@app.route('/airstaff_viewflights')
def airstaff_viewflights():
	return render_template('airstaff_viewflights.html')

#Define route for airstaff view flights: Nakeya Adams
@app.route('/airstaff_view_flights')
def airstaff_view_flights():
    username = session['username']
    cursor = conn.cursor()
    query = ('SELECT airline_name FROM airline_staff WHERE username = %s')
    cursor.execute(query, (username))
    airline_name = cursor.fetchone()
    query2 = ('Select airline_name, flight_number FROM flight WHERE departure_timestamp <= date_add(now(), INTERVAL 30 DAY) and departure_timestamp > CURRENT_DATE and airline_name = %s')
    cursor.execute(query2, (airline_name['airline_name']))
    data = cursor.fetchall()
    cursor.close()
    return render_template('airstaff_view_flights.html', data = data)

#Define route for airstaff view flights: Nakeya Adams
@app.route('/airstaff_view_flightsAuth', methods=['GET', 'POST'] )
def airstaff_view_flightsAuth():
    start_date = request.form['start']
    end_date = request.form['end']
    source_city = request.form['scity']
    destination_city = request.form['dcity']
    username = session['username']
    cursor = conn.cursor()
    query = ('SELECT airline_name FROM airline_staff WHERE username = %s')
    cursor.execute(query, (username))
    airline_name = cursor.fetchone()
    query2 = ('SELECT DISTINCT flight.airline_name, flight.flight_number FROM flight NATURAL JOIN airport WHERE flight.departure_code = (select airport.air_code from airport where (airport.air_city = %s or airport.air_name = %s)) and flight.arrival_code = (select airport.air_code from airport where (airport.air_city = %s or airport.air_name = %s)) and departure_timestamp > %s and departure_timestamp < %s and airline_name = %s')
    cursor.execute(query2, (source_city, source_city, destination_city, destination_city, start_date, end_date, airline_name['airline_name']))
    data = cursor.fetchall()
    cursor.close()
    return render_template('airstaff_view_flightsAuth.html', data = data)

#Define route for airstaff view flights: Nakeya Adams
@app.route('/airstaff_view_flightsAuth2', methods=['GET', 'POST'] )
def airstaff_view_flightsAuth2():
    airline_name = request.form['airline_name']
    flight_number = request.form['flight_number']
    cursor = conn.cursor()
    query = ('SELECT customer.name, customer.email FROM customer, flight, ticket, purchased_by WHERE flight.airline_name = %s and flight.flight_number = %s and flight.flight_number = ticket.flight_number and ticket.ticket_id = purchased_by.ticket_id and purchased_by.email = customer.email')
    cursor.execute(query, (airline_name, flight_number))
    data = cursor.fetchall()
    cursor.close()
    return render_template('airstaff_view_flightsAuth2.html', data = data, flight_number = flight_number)

# Search for flight status PAUL KIM
@app.route('/flight_statusAuth', methods=['GET', 'POST'] )
def flight_statusAuth():
	airline_name = request.form['airline']
	flight_number = request.form['f_number']
	arrival_date = request.form['a_date']
	departure_date = request.form['d_date']
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	if departure_date != None:
		query = ("SELECT DISTINCT flight.airline_name, flight.flight_number, flight.departure_timestamp, flight.arrival_timestamp, " +
				"flight.f_status, flight.base_price  FROM flight WHERE airline_name = %s and flight_number = %s and " +
				" date(arrival_timestamp) = %s" )
		cursor.execute(query, (airline_name, flight_number, arrival_date))
	else:
		query = ("SELECT DISTINCT flight.airline_name, flight.flight_number, flight.departure_timestamp, flight.arrival_timestamp, " +
				"flight.f_status, flight.base_price FROM flight WHERE airline_name = %s and flight_number = %s " +
				"and date(arrival_timestamp) = %s and date(departure_timestamp) = %s ")
		cursor.execute(query, (airline_name, flight_number, arrival_date, departure_date))

	data = cursor.fetchall()

	error = None
	if(data):
		conn.commit()
		cursor.close()
		return render_template('/flight_statusAuth.html', data = data)

	else:
		#If the previous query returns data, then user exists
		error = "No such flights exist"
		return render_template('/flight_statusAuth.html', data = data)

# Search for future flights PAUL KIM
@app.route('/customer_future_flightsAuth', methods=['GET', 'POST'] )
def customer_future_flightsAuth():
	source_city = request.form['scity']
	destination_city = request.form['dcity']
	departure_date = request.form['ddate']
	return_date = request.form['rdate']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	if return_date != None:
		query = ("SELECT DISTINCT flight.airline_name, flight.flight_number, flight.departure_timestamp, flight.arrival_timestamp, " +
				"flight.f_status, flight.base_price FROM flight NATURAL JOIN airport WHERE flight.departure_code = " +
				"(select airport.air_code from airport where (airport.air_city = %s or airport.air_name = %s)) and " +
				"flight.arrival_code = (select airport.air_code from airport where (airport.air_city = %s or airport.air_name = %s)) " +
				"and date(departure_timestamp) >= %s" )
		cursor.execute(query, (source_city, source_city, destination_city, destination_city, departure_date))
	else:
		query = ("SELECT DISTINCT flight.airline_name, flight.flight_number, flight.departure_timestamp, flight.arrival_timestamp, " +
				"flight.f_status, flight.base_price FROM flight NATURAL JOIN airport WHERE flight.departure_code = " +
				"(select airport.air_code from airport where (airport.air_city = %s or airport.air_name = %s)) and " +
				"flight.arrival_code = (select airport.air_code from airport where (airport.air_city = %s or airport.air_name = %s)) " + 
				"and departure_timestamp >= %s and arrival_timestamp <= %s" )
		cursor.execute(query, (source_city, destination_city, departure_date, return_date))
	data = cursor.fetchall()
	

	error = None
	if(data):
		email = session['email']
		# #airline_name = request.form['airline_name']
		# # flight_number = request.form['flight_number']
		# # departure_timestamp = request.form['departure_timestamp']
		# # arrival_timestamp =  request.form['arrival_timestamp']

		# num_ticket_query = "SELECT count(ticket_id) as count from ticket"
		# cursor.execute(num_ticket_query)
		# num_tickets = cursor.fetchone()
		# print(num_tickets['count'])


		conn.commit()
		cursor.close()
		error = "Incorrect Data"
		return render_template('/customer_future_flightsAuth.html', data = data, error=error)
	else:
		error = "No such flights exist"
		return render_template('/customer_future_flightsAuth.html', error=error)

# Search for future flights PAUL KIM
@app.route('/airstaff_future_flightsAuth', methods=['GET', 'POST'] )
def airstaff_future_flightsAuth():
	source_city = request.form['scity']
	destination_city = request.form['dcity']
	departure_date = request.form['ddate']
	return_date = request.form['rdate']
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	if return_date != None:
		query = ("SELECT DISTINCT flight.airline_name, flight.flight_number, flight.departure_timestamp, flight.arrival_timestamp, " +
				"flight.f_status, flight.base_price FROM flight NATURAL JOIN airport WHERE flight.departure_code = " +
				"(select airport.air_code from airport where (airport.air_city = %s or airport.air_name = %s)) and " +
				"flight.arrival_code = (select airport.air_code from airport where (airport.air_city = %s or airport.air_name = %s)) " +
				"and date(departure_timestamp) >= %s" )
		cursor.execute(query, (source_city, source_city, destination_city, destination_city, departure_date))
	else:
		query = ("SELECT DISTINCT flight.airline_name, flight.flight_number, flight.departure_timestamp, flight.arrival_timestamp, " +
				"flight.f_status, flight.base_price FROM flight NATURAL JOIN airport WHERE flight.departure_code = " +
				"(select airport.air_code from airport where (airport.air_city = %s or airport.air_name = %s)) and " +
				"flight.arrival_code = (select airport.air_code from airport where (airport.air_city = %s or airport.air_name = %s)) " + 
				"and departure_timestamp >= %s and arrival_timestamp <= %s" )
		cursor.execute(query, (source_city, destination_city, departure_date, return_date))

	data = cursor.fetchall()

	error = None
	if(data):
		conn.commit()
		cursor.close()
		return render_template('/airstaff_future_flightsAuth.html', data = data)
	else:
		#If the previous query returns data, then user exists
		error = "No such flights exist"
		return render_template('/airstaff_future_flightsAuth.html', {'data':data})

# Defines route for Track Spending: Paul Kim
@app.route('/track_spending', methods=['GET', 'POST'])
def track_spending():
	email = session['email']
	cursor = conn.cursor()
	query = ("SELECT SUM(ticket.sold_price) as last_year_spending FROM purchased_by NATURAL JOIN ticket WHERE " +
			 "purchased_by.email = %s and purchased_by.ticket_id = ticket.ticket_id and YEAR(purchase_timestamp) = " +
			 "YEAR(date_sub(current_date, INTERVAL 1 YEAR))")
	cursor.execute(query, (email))
	data = cursor.fetchone()

	query2 = ("SELECT MONTH(purchase_timestamp) as month, SUM(sold_price) as total FROM ticket NATURAL JOIN "+
			 "purchased_by WHERE purchase_timestamp >  Month(date_sub(current_date, INTERVAL 6 MONTH))and purchase_timestamp < current_date and purchased_by.email = %s " +
			 "GROUP BY MONTH(purchase_timestamp)")
	cursor.execute(query2, (email))
	data2 = cursor.fetchall()
	months = {1:0 , 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
	for elem in data2: 
		if elem['month'] in months:
			months[elem['month']] = elem['total']
	final_months = {}
	currentMonth = datetime.now().month
	lst_month = []
	for i in range(1,7):
		lst_month.append(currentMonth - i)
	for i in range(len(lst_month)):
		if lst_month[i] < 1:
			lst_month[i] += 12
	for i in lst_month:
		final_months[i] = months[i]
	cursor.close()
	return render_template('track_spending.html', data = data, data2 = final_months, currentMonth = currentMonth)

# Track Spending: Paul Kim
@app.route('/track_spendingAuth', methods=['GET', 'POST'] )
def track_spendingAuth():
    start_date = request.form['start']
    end_date = request.form['end']
    email = session['email']
    cursor = conn.cursor()
    query = ("SELECT MONTH(purchase_timestamp) as month, SUM(sold_price) as total FROM ticket NATURAL JOIN "+
			 "purchased_by WHERE purchase_timestamp > %s and purchase_timestamp < %s and purchased_by.email = %s " +
			 "GROUP BY MONTH(purchase_timestamp)")
    cursor.execute(query, (start_date, end_date, email))
    data = cursor.fetchall()
    cursor.close()
    return render_template('track_spendingAuth.html',data = data)

# Defines function for earned revenue: Paul Kim
@app.route('/earned_revenue')
def earned_revenue():
	username = session['username']

	cursor = conn.cursor()
	query = ("SELECT SUM(sold_price) as month_total FROM ticket, airline_staff WHERE ticket.airline_name = airline_staff.airline_name " + 
			"AND airline_staff.username = %s AND MONTH(purchase_timestamp) = month(date_sub(current_date, INTERVAL 1 MONTH)) and " +
			"YEAR(purchase_timestamp) = YEAR(current_date)" )
	cursor.execute(query,(username))
	data = cursor.fetchone()
	cursor2 = conn.cursor()
	
	query2 = ("SELECT SUM(sold_price) as year_total FROM ticket, airline_staff WHERE airline_staff.username = %s " +
				"AND Year(purchase_timestamp) = Year(date_sub(current_date, INTERVAL 1 YEAR))")
	cursor2.execute(query2,(username))
	data2 = cursor2.fetchone()

	query3 = "SELECT airline_name from airline_staff WHERE airline_staff.username = %s"
	cursor2.execute(query3,(username))
	data3 = cursor2.fetchone()

	cursor2.close()
	cursor.close()
	data.update(data2)
	return render_template('earned_revenue.html' , data = data, airline_name = data3 )

# Defines function for view reports auth: Paul Kim
@app.route('/view_reportsAuth', methods=['GET', 'POST'] )
def view_reportsAuth():
	username = session['username']
	year_month = request.form['last']
	start_date = request.form['start']
	end_date = request.form['end']
    
	cursor = conn.cursor()
	query3 = "SELECT airline_name from airline_staff WHERE airline_staff.username = %s"
	cursor.execute(query3,(username))
	airline_name = cursor.fetchone()
    
	if start_date != None:
		query = ("SELECT COUNT(purchase_timestamp) as number_tickets From Ticket, airline_staff WHERE ticket.airline_name = " +
				"airline_staff.airline_name AND airline_staff.username = %s AND  DATE(purchase_timestamp) >= %s " +
				"and DATE(purchase_timestamp) < %s;")
		cursor.execute(query, (username, start_date, end_date))
		data = cursor.fetchone()
		query = ("SELECT MONTH(purchase_timestamp) as month, COUNT(sold_price) as total FROM ticket, purchased_by, airline_staff " +
				 "WHERE purchase_timestamp > %s and purchase_timestamp < %s " + 
				 "AND ticket.ticket_id = purchased_by.ticket_id AND airline_staff.airline_name = ticket.airline_name " + 
				 "AND airline_staff.username = %s GROUP BY MONTH(purchase_timestamp);")
		cursor.execute(query, (start_date, end_date, username))

		table = cursor.fetchall()
		return render_template('view_reportsAuth.html' , data = data, table = table, airline_name = airline_name)
	else:
		if year_month == "y":
			query = ('SELECT COUNT(purchase_timestamp) as number_tickets From Ticket WHERE YEAR(purchase_timestamp) = YEAR(date_sub(current_date, INTERVAL 1 YEAR))')
			cursor.execute(query, ())
			data = cursor.fetchone()
			query = ('SELECT MONTH(purchase_timestamp) as month, COUNT(sold_price) as total FROM ticket NATURAL JOIN purchased_by WHERE YEAR(purchase_timestamp) = YEAR(date_sub(current_date, INTERVAL 1 YEAR))')
			cursor.execute(query, ())
			table = cursor.fetchall()
		else:
			query = ('SELECT COUNT(purchase_timestamp) as number_tickets From Ticket WHERE MONTH(purchase_timestamp) = month(date_sub(current_date, INTERVAL 1 MONTH)) and YEAR(purchase_timestamp) = YEAR(current_date)')
			cursor.execute(query, ())
			data = cursor.fetchone()
			query = ('SELECT MONTH(purchase_timestamp) as month, COUNT(sold_price) as total FROM ticket NATURAL JOIN purchased_by WHERE MONTH(purchase_timestamp) = month(date_sub(current_date, INTERVAL 1 MONTH)) and YEAR(purchase_timestamp) = YEAR(current_date)')
			cursor.execute(query,())
			table = cursor.fetchall()
	
	cursor.close()
	return render_template('view_reportsAuth.html' , data = data, table = table, airline_name = airline_name)

#Define route for frequent customer: Juliana Soranno
@app.route('/most_frequent_customer')
def most_frequent_customer():
	
	username = session['username']

	cursor1 = conn.cursor()
	query1 = ('SELECT airline_name FROM airline_staff where username = %s')
	cursor1.execute(query1, (username))
	data = cursor1.fetchone()
	airlineName = data['airline_name']
	
	cursor2 = conn.cursor()
	query2 = ('select distinct name, flight_number from customer, ticket , purchased_by ' +
				'where customer.email = purchased_by.email ' +
				'and ticket.ticket_id = purchased_by.ticket_id ' +
				'and name in (select distinct name from customer natural join purchased_by ' +
				'where customer.email = purchased_by.email ' +
				'and ticket_id in (select ticket_id from ticket where airline_name = %s ' +
				'and name_on_card IN( select name_on_card as most_frequent_customers  ' +
        		'FROM ticket GROUP BY name_on_card having count(name_on_card) =  ' +
        		'(select max(frequency) from (select name_on_card, count(name_on_card) as frequency  ' +
       			'from ticket group by name_on_card) as highest_frequency))));') 
	cursor2.execute(query2, (airlineName))

	frequentCustomers = cursor2.fetchall()
	for data in frequentCustomers:
		print(data["name"])

	cursor2.close()
	cursor1.close()
	return render_template('most_frequent_customer.html' , data = frequentCustomers)

#Define route and function for customer_viewflights : Nakeya Adams
@app.route('/customer_viewflights', methods=['GET', 'POST'] )
def customer_viewflights():
	email = session['email']
	query = ("SELECT email FROM purchased_by natural join ticket natural join customer WHERE customer.email = " +
			"purchased_by.email and purchased_by.email = %s;" )
	cursor = conn.cursor()
	cursor.execute(query, (email))
	data = cursor.fetchall()

	if(data):
		cursor2 = conn.cursor()
		query2 = ("select airline_name, flight_number, departure_timestamp, arrival_timestamp, f_status " +
				"from flight where flight_number in (SELECT flight_number FROM ticket natural join purchased_by where email = %s);") 

		cursor2.execute(query2, (email))
		flight_information = cursor2.fetchall()
		
		conn.commit()
		cursor2.close()

		return render_template('customer_viewflights.html', data = flight_information, email = email)

	else:
		error = "This user does not have any future flights"
		return render_template('customer_viewflights.html', error = error)

# #Airplane Staff change status of flights: Nakeya Adams
@app.route('/airstaff_change_statusAuth', methods=['GET', 'POST'])
def airstaff_change_statusAuth():
	username = session['username']

	airline_name = request.form['airline_name']
	flight_number = request.form['flight_number']
	departureTS = request.form['departure_timestamp']
	status = request.form['f_status']


	cursor = conn.cursor()
	query = "SELECT * FROM flight WHERE airline_name = %s AND flight_number = %s AND departure_timestamp = %s"
	cursor.execute(query, ( airline_name , flight_number, departureTS))
	data = cursor.fetchone()

	error = None
	
	if (data):
		query = "UPDATE flight SET f_status = %s WHERE airline_name = %s AND flight_number = %s AND departure_timestamp = %s"
		cursor.execute(query, (status, airline_name , flight_number, departureTS))

		query2 = ("SELECT airline_name, flight_number, departure_timestamp, arrival_timestamp, f_status FROM flight WHERE " +
				"airline_name = %s AND flight_number = %s AND departure_timestamp = %s;")
		
		cursor.execute(query2, (airline_name, flight_number, departureTS))
		updated_data = cursor.fetchone()
		conn.commit()
		cursor.close()
		return render_template('airstaff_change_status.html', data = data, updated_data = updated_data)
	else:
		error = "Flight does not exist"
		return render_template('airstaff_change_status.html' , error = error)

#Customers Give Ratings and Comments on their previous flights: Nakeya Adams
@app.route('/customer_ratings_commentsAuth', methods=['GET', 'POST'] )
def customer_ratings_commentsAuth():
	email = session['email']
	airline_name = request.form['airline_name']
	departure_timestamp = request.form['departure_timestamp']
	flight_number = request.form['flight_number']
	ratings = request.form['ratings']
	comments = request.form['comment']

	cursor = conn.cursor()
	query = ("SELECT * FROM purchased_by, ticket WHERE email = %s " +
			"and purchased_by.ticket_id = ticket.ticket_id ")
	cursor.execute(query, (email))
	data = cursor.fetchone()
	error = None
	if(data):
		query2 = ("INSERT INTO rates VALUES(%s, %s, %s, %s, %s, %s)")
		cursor.execute(query2, (airline_name, flight_number, departure_timestamp, email, comments, ratings))
		conn.commit()
		cursor.close()
		return render_template("customer_ratings_comments.html")
	else:
		error = "You have not been on this flight"
		return render_template("customer_ratings_comments.html", error = error)
	
#Defines function for Airline Staff viewing flight ratings: Nakeya Adams
@app.route('/airstaff_ratingsAuth', methods =['GET', 'POST'])
def airstaff_ratingsAuth():

	username = session['username']
	flight_number = request.form['flight_number']
	departure_timestamp = request.form['departure_timestamp']
	airline_name = request.form['airline_name']

	cursor1 = conn.cursor()
	query1 = ("SELECT AVG(ratings) as average FROM rates WHERE airline_name = %s AND departure_timestamp = %s " +
				"AND flight_number = %s ")
	cursor1.execute(query1, (airline_name , departure_timestamp, flight_number))
	avg_rating = cursor1.fetchone()

	if (avg_rating):
		query2 = ("SELECT email, ratings, comments, flight_number FROM rates " +
					" WHERE airline_name = %s AND departure_timestamp = %s " +
					"AND flight_number = %s " )

		cursor2 = conn.cursor()
		cursor2.execute(query2, (airline_name, departure_timestamp, flight_number))
		data2 = cursor2.fetchall()
		conn.commit()
		cursor2.close()
		return render_template("airstaff_ratings.html", data1 = avg_rating, data2 = data2)
	else:
		error = "This flight does not have any ratings"
		return render_template("/airstaff", error = error)

#Authenticates the customer_login: Juliana Soranno
@app.route('/customer_loginAuth', methods=['GET', 'POST'])
def customer_loginAuth():
	#grabs information from the forms

	username = request.form['email']
	c_password = request.form['c_password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE email = %s and c_password = %s'
	cursor.execute(query, (username, c_password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['email'] = username
		return redirect(url_for('customer_home'))
	else:
		#returns an error message to the html page
		error = 'Invalid email'
		return render_template('customer_login.html', error=error)

#Authenticates the airstaff_login:  Nakeya Adams
@app.route('/airstaff_loginAuth', methods=['GET', 'POST'] )
def airstaff_loginAuth():  
	#grabs information from the forms

	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM airline_staff WHERE username = %s and a_password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('airstaff_home'))
	else:
		#returns an error message to the html page
		error = 'Invalid username'
		return render_template('airstaff_login.html', error=error)

#Authenticates the customer_registerAuth: Juliana Soranno
@app.route('/customer_registerAuth', methods=['GET', 'POST'] )
def customer_registerAuth():
	#grabs information from the forms

	email = request.form['email']
	c_password = request.form['c_password']
	name = request.form['name']
	building_number = request.form['building_number']
	city = request.form['city']
	street = request.form['street']
	state = request.form['state']
	phone_number = request.form['phone_number']
	passport_expiration = request.form['passport_expiration']
	passport_number = request.form['passport_number']
	passport_country = request.form['passport_country']
	date_of_birth = request.form['date_of_birth']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE email = %s'
	cursor.execute(query, (email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('customer_registration.html', error = error)
	else:
		ins = 'INSERT INTO customer VALUES(%s, %s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (email, c_password, name, building_number, city, street, state, phone_number, 
							passport_expiration, passport_number, passport_country, date_of_birth ))
		conn.commit()
		cursor.close()
		return render_template('index.html')

#Authenticates the airstaff_registerAuth: Nakeya Adams
@app.route('/airstaff_registerAuth', methods=['GET', 'POST'] )
def airstaff_registerAuth():
	username = request.form['username']
	a_password = request.form['a_password']
	f_name = request.form['f_name']
	l_name = request.form['l_name']
	airline_date_of_birth = request.form['airline_date_of_birth']
	airline_name = request.form['airline_name']

	#cursor used to send queries
	airstaff_cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM airline_staff WHERE username = %s'
	airstaff_cursor.execute(query, (username))
	#stores the results in a variable
	data = airstaff_cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('airstaff_registration.html', error = error)
	else:
		ins = 'INSERT INTO airline_staff VALUES(%s, %s , %s, %s, %s, %s)'
		airstaff_cursor.execute(ins, (username, a_password, f_name, l_name, airline_date_of_birth, airline_name))
		conn.commit()
		airstaff_cursor.close()
		return render_template('index.html')

#Authenticates add_airport: Juliana Soranno
@app.route('/add_airportAuth', methods=['GET', 'POST'] )
def add_airportAuth():
	air_code = request.form['air_code']
	air_name = request.form['air_name']
	air_city = request.form['air_city']

	cursor = conn.cursor()
	query = 'SELECT * FROM airport WHERE air_code = %s'
	cursor.execute(query, (air_code))
	data = cursor.fetchone()
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This airport already exists"
		return render_template('add_airport.html', error = error)
	else:
		ins = 'INSERT INTO airport VALUES(%s, %s , %s)'
		cursor.execute(ins, (air_code, air_name, air_city))
		conn.commit()
		cursor.close()
		return render_template('add_airport.html')

#Authenticates add_airplane: Juliana Soranno
@app.route('/add_airplaneAuth', methods=['GET', 'POST'] )
def add_airplaneAuth():
	airline_name = request.form['airline_name']
	airplane_id = request.form['airplane_id']
	num_seats = request.form['num_seats']

	cursor = conn.cursor()
	query = 'SELECT * FROM airplane WHERE airline_name = %s and airplane_id = %s'
	cursor.execute(query, (airline_name , airplane_id))
	data = cursor.fetchone()
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This airplane already exists"
		return render_template('add_airplane.html', error = error)
	else:
		ins = 'INSERT INTO airplane VALUES(%s, %s , %s)'
		cursor.execute(ins, (airline_name, airplane_id, num_seats))
		conn.commit()
		cursor.close()
		return render_template('add_airplane.html')

#Authenticates add_flight: Juliana Soranno
@app.route('/add_flightAuth', methods=['GET', 'POST'] )
def add_flightAuth():
	#primary keys
	airline_name = request.form['airline_name']
	departure_timestamp = request.form['departure_timestamp']
	flight_number = request.form['flight_number']
	
	arrival_timestamp = request.form['arrival_timestamp']
	status = request.form['status']
	base_price = request.form['base_price']
	departure_code = request.form['departure_code']
	arrival_code = request.form['arrival_code']
	airplane_id = request.form['airplane_id']
	airplane_airline_name = request.form['airplane_airline_name']

	cursor = conn.cursor()
	query = 'SELECT * FROM flight WHERE airline_name = %s  and departure_timestamp = %s and flight_number = %s'
	cursor.execute(query, (airline_name , departure_timestamp, flight_number))
	data = cursor.fetchone()
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This flight already exists"
		return render_template('add_flight.html', error = error)
	else:
		ins = 'INSERT INTO flight VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )'
		cursor.execute(ins, (airline_name, flight_number, departure_timestamp, arrival_timestamp, status, base_price, 
								departure_code, arrival_code , airplane_id, airplane_airline_name))
		conn.commit()
		cursor.close()
		return render_template('add_flight.html')

#Logs out customer: Juliana Soranno
@app.route('/customer_logout')
def customer_logout():
	session.pop('email')
	return redirect('/')

#Logs out airstaff: Juliana Soranno
@app.route('/airstaff_logout')
def airstaff_logout():
	session.pop('username')
	return redirect('/')

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)