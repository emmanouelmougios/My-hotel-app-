def nights(arrive, leave):

    nights = []
    arrive = arrive.split("/")
    leave = leave.split("/")

    dayar = int(arrive[0])
    moar = int(arrive[1])
    yearr = int(arrive[2])
    
    dayle = int(leave[0])
    mole = int(leave[1])
    yele = int(leave[2])

    x=0
    nights = []

    if moar == 1 or moar == 3 or moar == 5 or moar == 7 or moar == 8 or moar ==10 or moar ==12:
        final = 31
    elif moar == 4 or moar == 6 or moar == 9 or moar == 11:
        final = 30
    elif moar == 2:
        final = 28

    if dayle < dayar:
        dayle = final + dayle

    for i in range(dayle-dayar):

        date = []

        day = dayar + x
        month = moar 
        year = yearr 

        if day > final:
            day = day - final
            if month == 12:
                month = 1
                year = yearr + 1
            else:
                month = moar + 1

        day = str(day)
        month = str(month)

        ########## standard ###########
        if len(day)==1:
            day = "0" + day
        if len(month)==1:
            month = "0" + month

        date.append(day)
        date.append("/")
        date.append(month)
        date.append("/")
        date.append(str(year))

        x+=1

        date = "".join(date)
        nights.append(date)
        dates = ' '.join(nights)
        ###############################

    return dates

print(nights("26/12/2021", "04/01/2022"))