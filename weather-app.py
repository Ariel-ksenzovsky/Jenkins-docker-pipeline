from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None
    error = None
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            # Simulated weather data for demonstration purposes
            weather_data = {
                'city': city,
                'temperature': "5°C",
                'description': "Partly cloudy",
                'icon': "01d"  # Example icon code
            }

    winter_facts = [
        "Snowflakes are unique, no two are exactly alike!",
        "The coldest temperature ever recorded was -128.6°F in Antarctica.",
        "Some animals, like bears, hibernate during winter to conserve energy.",
        "Winter is caused by the Earth's tilt, not its distance from the sun."
    ]

    return render_template('index.html', weather=weather_data, error=error, winter_facts=winter_facts)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

