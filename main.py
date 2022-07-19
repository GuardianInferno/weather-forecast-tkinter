# Weather Forecast
from tkinter import *
from tkinter import BOTH, IntVar
import requests
from PIL import ImageTk, Image
from io import BytesIO

# Define Window
root = Tk()
root.title("Weather Forecast")
root.geometry("400x400")
root.resizable(0, 0)

# Define fonts and colors
sky_color = "#76c3ef"
grass_color = "#aad207"
output_color = "#dcf0fb"
input_color = "#ecf2ae"
large_font = ("Arial", 13)
small_font = ("Arial", 8)


# Define Functions
# Define Functions
def search():
    """Use openweather API to look up the current weather conditions for city and/or zip"""
    global response

    url = 'https://api.openweathermap.org/data/2.5/weather?'
    api_key = '7721944a74a159eab3b104e4d4517775'

    # Search by city or zip code
    if search_method.get() == 1:
        querystring = {"q": city_entry.get(), "appid": api_key, "units": "imperial"}
        print(1)
    elif search_method.get() == 2:
        querystring = {"zip": city_entry.get(), "appid": api_key, "units": "imperial"}

    # Call API
    response = requests.request("GET", url, params=querystring)
    response = response.json()
    print(response)

    get_weather()
    get_icon()


def get_weather():
    # Gather specific data from API request
    city_name = response["name"]
    city_lat = str(response["coord"]["lat"])
    city_lon = str(response["coord"]["lon"])

    main_weather = response["weather"][0]["main"]
    description = response["weather"][0]["description"]

    temp = str(response["main"]["temp"])
    feels_like = str(response["main"]["feels_like"])
    temp_min = str(response["main"]["temp_min"])
    temp_max = str(response["main"]["temp_max"])
    humidity = str(response["main"]["humidity"])

    # Update output labels
    city_info_label.config(text=city_name + "(" + city_lat + ", " + city_lon + ")", font=large_font, bg=output_color)
    main_weather_label.config(text=main_weather, bg=output_color)
    description_label.config(text=description, bg=output_color)
    temp_label.config(text=temp, bg=output_color)
    feels_label.config(text=feels_like, bg=output_color)
    min_label.config(text=temp_min, bg=output_color)
    max_label.config(text=temp_max, bg=output_color)
    humid_label.config(text=humidity, bg=output_color)


def get_icon():
    """Get the appropriate weather icon from API response"""
    global img

    # Get the icon id from API response.
    icon_id = response['weather'][0]['icon']

    # Get the icon from the correct webiste
    url = 'http://openweathermap.org/img/wn/{icon}.png'.format(icon=icon_id)

    # Make a request at the url to download the icon; stream=True automatically dl
    icon_response = requests.get(url, stream=True)

    # Turn into a form tkinter/python can use
    img_data = icon_response.content
    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))

    # Update label
    photo_label.config(image=img, bg=output_color)


# Define Layout
# Create Frames
sky_frame = Frame(root, bg=sky_color, height=250)
grass_frame = Frame(root, bg=grass_color)
sky_frame.pack(fill=BOTH, expand=True)
grass_frame.pack(fill=BOTH, expand=True)

output_frame = LabelFrame(sky_frame, bg=output_color, width=325, height=225)
input_frame = LabelFrame(grass_frame, bg=input_color, width=325)
output_frame.pack(pady=30)
output_frame.propagate(0)
input_frame.pack(pady=15, fill=X)

city_info_label = Label(output_frame, font=large_font)
main_weather_label = Label(output_frame, font=small_font)
description_label = Label(output_frame, font=small_font)
temp_label = Label(output_frame, font=small_font)
feels_label = Label(output_frame, font=small_font)
min_label = Label(output_frame, font=small_font)
max_label = Label(output_frame, font=small_font)
humid_label = Label(output_frame, font=small_font)
photo_label = Label(output_frame)

city_info_label.pack(pady=8)
main_weather_label.pack()
description_label.pack()
temp_label.pack()
feels_label.pack()
min_label.pack()
max_label.pack()
humid_label.pack()
photo_label.pack()

city_entry = Entry(input_frame, font=large_font)
city_entry.grid(row=0, column=0, padx=5, pady=10)

search_method = IntVar()
search_method.set(1)
radio1 = Radiobutton(input_frame, font=small_font, text="Search by city name", variable=search_method, value=1)
radio1.grid(row=1, column=0)

radio2 = Radiobutton(input_frame, font=small_font, text="Search by zip code", variable=search_method, value=2)
radio2.grid(row=1, column=1)

submit = Button(input_frame, font=large_font, text='Submit', bg=input_color, command=lambda: search())
submit.grid(row=0, column=1, pady=10)
# Run the windows main loop
root.mainloop()