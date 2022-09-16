# import required modules
from configparser import ConfigParser
import requests
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from firebase_connect import add_user

# extract key from the
# configuration file
config_file = "config.ini"
config = ConfigParser()
config.read(config_file)
api_key = config['key']['api']
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'


# explicit function to get
# weather details
def getweather(city):
    result = requests.get(url.format(city, api_key))

    if result:
        json = result.json()
        city = json['name']
        country = json['sys']
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        weather1 = json['weather'][0]['main']
        final = [city, country, temp_kelvin,
                 temp_celsius, weather1]
        return final
    else:
        print("No Content Found")


# explicit function to
# search city
def search():
    city = city_text.get()
    weather = getweather(city)
    if weather:
        location_lbl['text'] = '{} ,{}'.format(weather[0], weather[1])
        temperature_label['text'] = str(weather[3]) + " Degree Celsius"
        weather_l['text'] = weather[4]
    else:
        messagebox.showerror('Error', "Could not find {}".format(city))

def register(email,username,password,location):

    # check whether the particular location exists or not
    weather = getweather(location.get())
    if weather:

        if (email.get().strip() == "" or username.get().strip() == "" or password.get().strip() == ""):
            messagebox.showerror('Error',
                                 "Please add correct details")
        else:
            add_user(str(email.get()),str(username.get()),str(password.get()),str(location.get()))
            messagebox.showinfo('Done', 'Done')
    else:
        messagebox.showerror('Error', "Cannot find {}. Please enter a valid location to register".format(location.get()))


def subscribe():
    top = Toplevel(app)
    top.geometry("300x300")
    top.title("Popup Window")
    # add labels, buttons and text
    email_lbl = Label(top, text="Enter Email", font={'bold', 8})
    email_lbl.pack()
    email = StringVar()
    email_entry = Entry(top, text="Email", textvariable=email)
    email_entry.pack()
    username_lbl = Label(top, text="Enter username", font={'bold', 8})
    username_lbl.pack()
    username = StringVar()
    username_entry = Entry(top, text="username", textvariable=username)
    username_entry.pack()
    password_lbl = Label(top, text="Enter Password", font={'bold', 8})
    password_lbl.pack()
    password=StringVar()
    password_entry=Entry(top, text="password", textvariable=password)
    password_entry.pack()
    location_lbl = Label(top, text="Enter Location", font={'bold', 8})
    location_lbl.pack()
    location=StringVar()
    location_entry= Entry(top, text="Location", textvariable=location)
    location_entry.pack()
    User_add = Button(top, text="Subscribe",
                        width=12, command=lambda: register(email_entry,username_entry,password_entry,location_entry))
    User_add.pack()


# Driver Code
# create object
app = Tk()
# add title
app.title("Weather App")
# adjust window size
app.geometry("750x250")

# add labels, buttons and text
city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()
Search_btn = Button(app, text="Search Weather",
                    width=12, command=search)
Search_btn.pack()
location_lbl = Label(app, text="")
location_lbl.pack()
temperature_label = Label(app, text="")
temperature_label.pack()
weather_l = Label(app, text="")
weather_l.pack()
ttk.Button(app, text="Subscribe to us",
                    width=30, command=subscribe).pack()
app.mainloop()
