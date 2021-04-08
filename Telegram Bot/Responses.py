from datetime import datetime

def remove_stuff(x):
    string = x.replace("(","").replace(")","").replace(",","").replace(" ","").replace("'","")   #remove unwanted stuff
    return string

def sample_reponses(input_text):
    user_message = str(input_text).lower() #user dont have to worry about case sensitive text

    if user_message in ("hello", "hi", "sup", "room1", "Room1"):
        
        with open("data.txt","r") as f:
            lines = f.read().splitlines()
            last_line = lines[-1]
            edit = last_line.split(" ")
            x = edit[-6]
            xx = edit[-5]
            xxx = edit[-4]
            val1 = remove_stuff(x)
            val2 = remove_stuff(xx)
            val3 = remove_stuff(xxx)
            
            msgs = "Room1 "+ "\n" + "Capacity: " + val1 + "\n" + "Temperature: "+ val2 + "\n" + "Humidity: " + val3
            print(last_line)
        return msgs
        
    if user_message in ("hello", "hi", "sup", "room2", "Room2"):
        
        with open("data2.txt","r") as f:
            lines = f.read().splitlines()
            last_line = lines[-1]
            edit = last_line.split(" ")
            x = edit[-6]
            xx = edit[-5]
            xxx = edit[-4]
            val1 = remove_stuff(x)
            val2 = remove_stuff(xx)
            val3 = remove_stuff(xxx)
            
            
            msgs = "Room2 "+ "\n" + "Capacity: " + val1 + "\n" + "Temperature: "+ val2 + "\n" + "Humidity: " + val3
            
            print(last_line)
        return msgs
    else:
        return ""