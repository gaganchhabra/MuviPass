# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import smtplib
from datetime import datetime

def index():

    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    #response.flash = T("Welcome to web2py!")
    #form=FORM('Movie name:  ', SELECT(_name='movie'),requires=IS_NOT_EMPTY())
    ##auth.wiki()
    #cityList=list()
    #for row in db().select(db.City.ALL):
    #    cityList.append(row.cityName)
    cities=db().select(db.City.ALL)
    city=request.vars.city
    theatre=request.vars.theatre
    movie=request.vars.movie
    time=request.vars.time
    qty=request.vars.quantity
    
    
    #cronFun()
    
    #print  qty, "hehkasjhfddkhsfkjsdhkj"
    
    
    #if request.vars.city!="default":
    #    session.cityName=request.vars.city
    #if request.vars.theatre!="default":
    #    session.theatreName=request.vars.theatre
    #if request.vars.movie!="default":
    #    session.movieName=request.vars.movie
    #if request.vars.time!="default":
    #    session.time=request.vars.time
    theatres=list()
    if city!="default":
        theatresId=db((db.City.cityName==request.vars.city)).select(db.City.theatreId)
        for theatreIterator in theatresId:
            theatresName=(db((db.Theatre.theatreId==theatreIterator.theatreId)).select(db.Theatre.theatreName))
            for row in theatresName:
                theatres.append(row.theatreName)
    #for row in db().select(db.Theatre.ALL):
    #    theatreList.append(row.theatreName)t
    movies=list()
    if theatre!="default":
        moviesId=db((db.Theatre.theatreName==theatre)).select(db.Theatre.movieId)
        for movieIterator in moviesId:
            movieName=(db((db.Movie.movieId==movieIterator.movieId)).select(db.Movie.movieName))
            for row in movieName:
                movies.append(row.movieName)
    #for row in db().select(db.Movie.ALL):
    #    lis.append(row.movieName)
    currentTime=datetime.time(datetime.now())
    print "Current Time", currentTime
    showTime=list()
    if movie!="default" and city!="default" and theatre!="default":
        theatresId=db((db.City.cityName==city)).select(db.City.theatreId)
        moviesId=db((db.Theatre.theatreName==theatre)).select(db.Theatre.movieId)
        for it1 in theatresId:
            for it2 in moviesId:
                showTimes=db((db.ShowTime.theatreId==it1.theatreId)&(db.ShowTime.movieId==it2.movieId)).select()
                for timeIterator in showTimes:
                    if timeIterator.showTime>currentTime:
                        showTime.append(timeIterator.showTime)
    #for row in db().select(db.ShowTime.ALL):
    #    showTimeList.append(row.showTime)
    return dict(message='',movies=movies,cities=cities,theatres=theatres,showTime=showTime,city=city,theatre=theatre,movie=movie,time=time)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

def seats():
    #print request.vars.city, request.vars.theatre, request.vars.movie
    # print "this is the quantututiutuitg :   ",session.qty
    thId=db((db.Theatre.theatreName==request.vars.theatre)).select() #db.Theatre.theatreId
    mvId=db((db.Movie.movieName==request.vars.movie)).select()  #db.Movie.movieId
    for thRow in thId:
        x=thRow.theatreId
    for mvRow in mvId:
        y=mvRow.movieId

    session.shwtym=request.vars.time
    session.city=request.vars.city
    session.theatreName=request.vars.theatre
    session.movieName=request.vars.movie
    
    session.theatre=x
    session.movie=y
    session.quantity=request.vars.quantity
    
    booked_String=""
    listOfBookedSeats=list()
    
    allBookings=db((db.ShowDetails.movieId==y)&(db.ShowDetails.theatreId==x)&(db.ShowDetails.showTime==session.shwtym)).select()
    if len(allBookings) == 0 :
        return dict(booked=listOfBookedSeats,qty=request.vars.quantity)
    for foo in allBookings:
        booked_String=foo.seats
    #print booked_String
    
    listOfBookedSeats=booked_String.split(',')
    listOfBookedSeats=listOfBookedSeats[:len(listOfBookedSeats)-1]
    
    for dodo in range(0,len(listOfBookedSeats)):
        listOfBookedSeats[dodo]=int(listOfBookedSeats[dodo])
    
    return dict(booked=listOfBookedSeats,qty=request.vars.quantity)


def confirm():
    # print "this is what i neeeeeeeeeeeeeed :",len(request.vars.checks)
    #   session.city
    #   session.theatre
    #   session.movie
    #   session.quantity
    selectedSeats=request.vars.seatsList.split(',')
    selectedSeats=selectedSeats[:len(selectedSeats)-1]
    for i in range(0,len(selectedSeats)):
        selectedSeats[i]=1+int(selectedSeats[i])

    session.userSelectedSeats=selectedSeats
    print session.userSelectedSeats
    userKnownSeats=mapTickets(selectedSeats)
    
    allBookings=db((db.ShowDetails.movieId==session.movie)&(db.ShowDetails.theatreId==session.theatre)&(db.ShowDetails.showTime==session.shwtym)).select()
    booked_String=""
    if len(allBookings)!=0:
        for foo in allBookings:
            booked_String=foo.seats
        #print booked_String
        for itm in  selectedSeats:
            booked_String=booked_String+str(itm)+','
    else:
        for itm in  selectedSeats:
            booked_String= str(itm) + "," + booked_String
    
    #booked_String=booked_String[:len(booked_String)-1]
    session.bookedSeats=booked_String
    
    
    #wrote the update query after redirection ;) !!
    session.usersTickets=userKnownSeats
    return dict(seats=userKnownSeats)


def mapTickets(selectedSeats):
    userFamiliarSeats=list()
    row=''
    for seat in selectedSeats:
        if seat >= 1 and seat <= 20:
            row='A'
        elif  seat >= 21 and seat <= 40 : 
            row='B'
        elif  seat >= 41 and seat <= 60 : 
            row='C'
        elif  seat >= 61 and seat <= 80 : 
            row='D'
        elif  seat >= 81 and seat <= 100 : 
            row='E'
        elif  seat >= 101 and seat <= 120 : 
            row='F'
        elif  seat >= 121 and seat <= 140 : 
            row='G'
        elif  seat >= 141 and seat <= 160 : 
            row='H'
        elif  seat >= 161 and seat <= 180 : 
            row='I'
        elif  seat >= 181 and seat <= 200 : 
            row='J'
        
        seatNumInRow=seat % 20
        if seatNumInRow == 0:
            seatNumInRow=20
        seatNum=row+str(seatNumInRow)
        userFamiliarSeats.append(seatNum)
        userFamiliarSeats.sort()
    return userFamiliarSeats


def final():
    # make entry in the booking table and generate the booking id
    # Booking.bookingId	Booking.movieId	Booking.theatreId

    #session.movie
    #session.theatre
    rows=db(db.Booking.bookingId>0).select()
    bIds=list()
    
    if len(rows)!=0:
        for row in rows:
            bIds.append(row.bookingId)
        tempBId=max(bIds)
        nextBId=tempBId+1
    else:
        nextBId=890890
        pass
    
    seatss=list()
    for x in session.userSelectedSeats:
        seatss.append(str(x))
    
    seatss=",".join(seatss)    
    db.Booking.insert(bookingId=nextBId,movieId=session.movie,theatreId=session.theatre,showTime=session.shwtym,seats=seatss)
    
    #update the seats booked
    if len(db((db.ShowDetails.movieId==session.movie)&(db.ShowDetails.theatreId==session.theatre)&(db.ShowDetails.showTime==session.shwtym)).select()) > 0:
        db((db.ShowDetails.movieId==session.movie)&(db.ShowDetails.theatreId==session.theatre)&(db.ShowDetails.showTime==session.shwtym)).update(seats=session.bookedSeats)
    else:
        db.ShowDetails.insert(movieId=session.movie, theatreId=session.theatre,showTime=session.shwtym,seats=session.bookedSeats)

    # Initialize SMTP server
    server=smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login('muvipass','project123')
    # Send email
    senddate=datetime.strftime(datetime.now(), '%Y-%m-%d')
    subject="Ticket Booking Notification"
    m="Date: %s\r\nFrom: %s\r\nTo: %s\r\nSubject: %s\r\nX-Mailer: My-Mail\r\n\r\n" % (senddate, 'muvipass@gmail.com', request.vars.email, subject)
    msg='Dear User,\n\t Your ticket has been booked. Following are the details:\n\n\tBooking Id: ' + str(nextBId) + '\n\tTheatre: '+ str(session.theatreName) + '\n\tMovie: '+ str(session.movieName) + '\n\tShow Time: ' + str(session.shwtym) + '\n\tSeats: ' + ", ".join(session.usersTickets)
    server.sendmail('muvipass@gmail.com', request.vars.email, m+msg)
    server.quit()
    
    
    data=TABLE(TR(TD('Booking Id: '),TD(nextBId)),TR(TD('Theatre: '),TD(session.theatreName)),TR(TD('Movie: '),TD(session.movieName)),TR(TD('Show Time: '),TD(session.shwtym)),TR(TD('Seats: '),TD(", ".join(session.usersTickets))))
    
    ##deleteing the attributes set for the session i.e. invalidating the session
    
    del session.shwtym
    del session.city
    del session.movie
    del session.theatre
    del session.theatreName
    del session.movieName
    del session.bookedSeats
    del session.usersTickets
    del session.userSelectedSeats
    return dict(data=data)



def adminLogin():
    redirect(URL('..','admin','default'))
    return dict()


def gallery():
    return dict()

def cancel():
    return dict()

def cronFun():
    # Booking.bookingId	Booking.movieId	Booking.theatreId	Booking.showTime	Booking.seats
    selected=db(db.Booking.bookingId>0).select()
    for row in selected:
        db.Booking_Archieve.insert(bookingId=row.bookingId,movieId=row.movieId,theatreId=row.theatreId,showTime=row.showTime,seats=row.seats)
    #ShowDetails.movieId	ShowDetails.theatreId	ShowDetails.showTime	ShowDetails.seats

    selected2=db(db.ShowDetails.movieId>0).select()
    for row2 in selected2:
        db.ShowDetails_Archieve.insert(movieId=row2.movieId,theatreId=row2.theatreId,showTime=row2.showTime,seats=row2.seats)
    db(db.Booking.bookingId>0).delete()
    db(db.ShowDetails.movieId>0).delete()
    db.commit()
