def detect_line(x,y,lookup:callable,special=False,color=None):
    '''Given an x and y position, as well as the function lookup, this function will search all the squares around it to find lines of gems.'''
    count = 0
    usedsquares = list()
    curx = x
    cury = y
    #Moves down as far as there are matches
    if special:
        col = color
    else:
        col = lookup(x,y)
    while (col if (curx,cury) == (x,y) else lookup(curx,cury)) == col:
        count += 1
        usedsquares.append([curx,cury]) #add the current match to the list
        cury += 1 #move it down one
        if cury >= 7: break #stop it from overflowing
    if count != 0:
        curx = x
        cury = y-1 #subtracts one so it doesnt double count the first one
        #Once it has finished if it found anything it goes back up to look for other matches
        while (col if (curx,cury) == (x,y) else lookup(curx,cury))  == col:
            if cury < 0: break
            count += 1 
            usedsquares.append([curx,cury]) #add the current match to the list
            cury -= 1 #move it up one row
    
    #Does it again for the up direction, doesnt need to check for down because it just did that
    while (col if (curx,cury) == (x,y) else lookup(curx,cury))  == col:
        if cury < 0: break
        count += 1 
        usedsquares.append([curx,cury]) #add the current match to the list
        cury -= 1 #move it up one row
    if count == 5: #Return if already a diamond
        return usedsquares, "V"
    if count < 3: #If there were no lines that way they do not count
        count == 0
        usedsquares.clear()
    #now for the horizontal lines
    xcount = 0 #resetting things for the horizontal check
    xusedsquares = list()
    curx = x
    cury = y
    #checking for anything to the right
    while (col if (curx,cury) == (x,y) else lookup(curx,cury))  == col:
        xcount += 1
        xusedsquares.append([curx,cury]) #add the current match to the list
        curx += 1 #move it right one column
        if curx >= 7: break
    if xcount != 0:
        curx = x-1 #subtracts one to avoid double counting
        cury = y
        #Go back to the left to look for more matches
        while (col if (curx,cury) == (x,y) else lookup(curx,cury))  == col:
            if curx < 0: break
            xcount += 1
            xusedsquares.append([curx,cury]) #add the current match to the list
            curx -= 1 #move it back left
    if xcount < 3: #If there were no lines that way they do not count
        xcount == 0
        xusedsquares.clear()
    if xcount == 5: #Return if already a diamond
        return xusedsquares, "H"
    if len(xusedsquares)+len(usedsquares) >= 6:
        return xusedsquares+usedsquares,"HV"
    elif len(xusedsquares) >= 3:
        return xusedsquares,"H"
    elif len(usedsquares) >= 3:
        return usedsquares,"V"
    #Now to check for left on its own
    while (col if (curx,cury) == (x,y) else lookup(curx,cury))  == col:
        if curx < 0: break
        xcount += 1
        xusedsquares.append([curx,cury]) #add the current match to the list
        curx -= 1 #move it left one column
    if xcount == 5:
        return xusedsquares, "V"
    if len(xusedsquares)+len(usedsquares) >= 6:
        return xusedsquares+usedsquares,"HV"
    elif len(xusedsquares) >= 3:
        return xusedsquares,"H"
    elif len(usedsquares) >= 3:
        return usedsquares,"V"
    return [],"0"