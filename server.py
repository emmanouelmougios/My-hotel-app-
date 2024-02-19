from flask import Flask
from flask import render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from nightdates import nights
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booking.db'

#database creation
db = SQLAlchemy(app)


class Booking(db.Model):
    #categorizing the database
    id = db.Column("id", db.Integer, primary_key=True)
    fname = db.Column("fname", db.String(20), nullable=False)
    lname = db.Column("lname", db.String(20), nullable=False)
    arrive = db.Column("arrive", db.String(20), nullable=False)
    leave = db.Column("leave", db.String(20), nullable=False)
    people = db.Column("people", db.Integer(), nullable=False)
    nights = db.Column("nights", db.String(500), nullable=False)

    def __init__(self, fname, lname, arrive, leave, people, nights):
        self.fname = fname
        self.lname = lname
        self.arrive = arrive
        self.leave = leave
        self.people = people
        self.nights = nights

##########################################################################

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

################### HOME PAGE ##########################################
@app.route('/')
def hello_world():
    return render_template('home.html')

############################# BOOKING PAGE #############################################

@app.route('/book', methods= ['POST', 'GET'])
def book():  
    if request.method == "POST":

        #ROOMS#########
        two = 15
        three = 10
        four = 5
        ###############

        firstname = (request.form["firstname"]).upper()    # receiving the data from the booking forms
        lastname = (request.form["lastname"]).upper()
        arrive = request.form["arrival"]
        leave = request.form["leave"]
        people = request.form["people"]


        if firstname=="" or lastname=="" or arrive=="" or leave=="":
            return render_template('bookerror.html')
        else:
            dates = nights(arrive, leave)             # finding the dates that are taken from the client
            night_dates = dates.split(' ')

            arrive = arrive.split('/')
            day = arrive[0]
            month = arrive[1]
            year = arrive[2]
            if len(day)==1:
                day = "0" + day
            if len(month)==1:
                month = "0" + month
            if len(year)==2:
                year = "20" + year
                
            arrive = []
            day = str(day)
            month = str(month)
            arrive.append(day)
            arrive.append(month)
            arrive.append(str(year))
            arrive = '/'.join(arrive)

            leave = leave.split('/')
            day = leave[0]
            month = leave[1]
            year = leave[2]
            if len(day)==1:
                day = "0" + day
            if len(month)==1:
                month = "0" + month
            if len(year)==2:
                year = "20" + year
                
            leave = []
            day = str(day)
            month = str(month)
            leave.append(day)
            leave.append(month)
            leave.append(str(year))
            leave = '/'.join(leave)

            #adding the data to the database if the rooms are available

            #2
            if people == '2':          
                for i in range(len(night_dates)):
                    rooms = 0
                    night = night_dates[i]
                    bookings = Booking.query.all()
                    for j in bookings:
                        if night in j.nights:
                            if int(people) == j.people:
                                rooms += 1
                                if rooms == two:
                                    return render_template('booked.html', value=["double rooms", night])
                                    break
                                else:
                                    continue
                if rooms<two:
                    new_first = Booking(fname = firstname, lname = lastname, arrive = arrive , leave = leave , people = people, nights = dates)

            #3
            if people == '3':          
                for i in range(len(night_dates)):
                    rooms = 0
                    night = night_dates[i]
                    bookings = Booking.query.all()
                    for j in bookings:
                        if night in j.nights:
                            if int(people) == j.people:
                                rooms += 1
                                if rooms == three:
                                    return render_template('booked.html', value=["three-bed rooms", night])
                                    break
                                else:
                                    continue
                if rooms<three:
                    new_first = Booking(fname = firstname, lname = lastname, arrive = arrive , leave = leave , people = people, nights = dates)

            #4
            if people == '4':          
                for i in range(len(night_dates)):
                    rooms = 0
                    night = night_dates[i]
                    bookings = Booking.query.all()
                    for j in bookings:
                        if night in j.nights:
                            if int(people) == j.people:
                                rooms += 1
                                if rooms == four:
                                    return render_template('booked.html', value=["four-bed rooms", night])
                                    break
                                else:
                                    continue


                if rooms<four:
                    new_first = Booking(fname = firstname, lname = lastname, arrive = arrive , leave = leave , people = people, nights = dates)

        try:
            db.session.add(new_first)                         
            db.session.commit()
            return render_template('bookdone.html', value=firstname)
        except:
            return render_template('bookerror.html')
    else:
        return render_template('book.html')

############################### MEMBER PAGE ###########################################
    
@app.route('/member', methods= ['POST', 'GET'])
def member():
    if request.method == "POST":
        #ROOMS#########
        two = 15
        three = 10
        four = 5
        ###############
        try:
            firstname = ""
            lastname = ""
            arrive = ""
            leave = ""
            firstname = (request.form["firstname"]).upper()
            lastname = (request.form["lastname"]).upper()
            arrive = request.form["arrival"]
            leave = request.form["leave"]

        except:
            
            # find and print the available rooms on the date the user selects

            date = request.form["datefree"]

            if date!= "":

                double=two
                triple=three
                fo = four

                date = date.split('/')
                day = date[0]
                month = date[1]
                year = date[2]
                if len(day)==1:
                    day = "0" + day
                if len(month)==1:
                    month = "0" + month
                if len(year)==2:
                    year = "20" + year
                    
                date = []
                day = str(day)
                month = str(month)
                date.append(day)
                date.append(month)
                date.append(str(year))
                date = '/'.join(date)

                bookings = Booking.query.all()
                for j in bookings:
                    if date in j.nights:
                        if j.people == 2:
                            double-=1
                        if j.people == 3:
                            triple-=1
                        if j.people == 4:
                            fo-=1

                double = "Double rooms: " + str(double)
                triple = "3-bed rooms: " + str(triple)
                fo = "4-bed rooms: " + str(fo)

                return render_template('member.html', values = [date, double, triple, fo])

        found_booking = []
        
        if firstname != "":
            found_booking = Booking.query.filter_by(fname=firstname).all()
        elif lastname != "":
            found_booking = Booking.query.filter_by(lname=lastname).all()
        elif arrive != "":
            found_booking = Booking.query.filter_by(arrive=arrive).all()
        elif leave != "":
            found_booking = Booking.query.filter_by(leave=leave).all()

        if len(found_booking)==0:
            return render_template('membernotfound.html')
        else:
            return render_template('memberfound.html', values=found_booking)

    else:
        return render_template('member.html', values = ["", "", "", ""])

##########################################################################

@app.route('/memberfound', methods= ['POST', 'GET'])
def memberfound():
    return render_template('memberfound.html')

############################# FACILITIES PAGE #############################################

@app.route('/facilities', methods= ['POST', 'GET'])
def facilities():
    return render_template('facilities.html')

########################## CANCEL BOOKING PAGE ################################################

@app.route('/cancel', methods= ['POST', 'GET'])
def cancel(): 

    if request.method == "POST":

        values = ["", "", ""]
        firstname = (request.form["firstname"]).upper()
        lastname = (request.form["lastname"]).upper()
        arrive = request.form["arrival"]
        leave = request.form["leave"]
        people = request.form["people"]

        if firstname=="" or lastname=="" or arrive=="" or leave=="":
            values[0] = "Cancellation error. Make sure you fill all the forms."
            return render_template('cancelresults.html', value = values)
        else:
            try:

                arrive = arrive.split('/')
                day = arrive[0]
                month = arrive[1]
                year = arrive[2]
                if len(day)==1:
                    day = "0" + day
                if len(month)==1:
                    month = "0" + month
                if len(year)==2:
                    year = "20" + year
                    
                arrive = []
                day = str(day)
                month = str(month)
                arrive.append(day)
                arrive.append(month)
                arrive.append(str(year))
                arrive = '/'.join(arrive)

                leave = leave.split('/')
                day = leave[0]
                month = leave[1]
                year = leave[2]
                if len(day)==1:
                    day = "0" + day
                if len(month)==1:
                    month = "0" + month
                if len(year)==2:
                    year = "20" + year
                    
                leave = []
                day = str(day)
                month = str(month)
                leave.append(day)
                leave.append(month)
                leave.append(str(year))
                leave = '/'.join(leave)

                cancelation = Booking.query.filter_by(fname = firstname, lname = lastname, arrive = arrive , leave = leave , people = people).first()
                db.session.delete(cancelation)
                db.session.commit()
                values[0] = "Your cancellation was successful"
                values[1] = firstname + "."
                return render_template('cancelresults.html', value=values)
            except:
                values[0] = "Cancellation error. This reservation was not found."
                return render_template('cancelresults.html', value = values)
        
    else:
        return render_template('cancel.html')

##########################################################################

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

# py -3 -m venv venv
# Set-ExecutionPolicy Unrestricted -Scope CurrentUser -Force
# venv\Scripts\activate