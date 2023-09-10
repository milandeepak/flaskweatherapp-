import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['DEBUG'] = True


cities = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city_name = request.form.get('city')

        if city_name:
            url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=f8b794366a2605ac9b420df813e61e25'
            
            r = requests.get(url.format(city_name)).json()

            weather_data = {
                'city': city_name,
                'temperature': r['main']['temp'],
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon'],
            }

            cities.append(weather_data)


    cities_per_row = [cities[i:i + 5] for i in range(0, len(cities), 5)]

    return render_template('index.html', cities_per_row=cities_per_row)

@app.route('/remove/<int:index>')
def remove_city(index):
    if 0 <= index < len(cities):
        cities.pop(index)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
