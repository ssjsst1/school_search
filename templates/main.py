# Code developed bY Ashutosh Nayak on 19-09-2023
# This project display the list of schools based on search criteria
# For this I have created 2 html pages and one python script pages (index.html,schoollist.html and main.py)
# This is the very interactive project user can search and come back to the main page

# Import required libraries
import requests  # Library for making HTTP requests
from bs4 import BeautifulSoup  # Library for web scraping
from flask import Flask, render_template, request, redirect, url_for, \
    Response  # Flask web framework for building web applications
import csv  # Library for working with CSV files

# Create a Flask web application instance
main = Flask(__name__)

# Number of school names to display in the page
maxSchdisplay = 20


# Define a function for searching schools on Google
def g_search(query):
    # Construct the Google search URL with the given query
    urls = f"https://www.google.com/search?q={query.replace(' ', '+')}+schools"

    # Set headers to the web browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    # Send an HTTP GET request to Google search for schools
    response = requests.get(urls, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('h3')
        schools = [result.text for result in results]
        # Return the list of school names
        return schools
    else:
        return None


# Create a Flask route for the root URL ('/')
@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city_name = request.form['city_name']
        if city_name:
            # Redirect to the 'schoollist' route with the city_name as a parameter
            return redirect(url_for('schoollist', city_name=city_name))
    # Render the 'index.html' template if the request method is GET
    return render_template('index.html')


# Create a route for displaying the school list
@main.route('/schoollist/<city_name>', methods=['GET', 'POST'])
def schoollist(city_name):
    if request.method == 'POST':
        city_name = request.form['city_name']
        if city_name:
            # Redirect to the 'schoollist' route with the updated city_name
            return redirect(url_for('schoollist', city_name=city_name))

    # Calling the g_search function to search for schools based on the city name
    schools = g_search(city_name)
    schools = schools[:maxSchdisplay]

    # Render the 'schoollist.html' template with the city_name and schools data
    return render_template('schoollist.html', city_name=city_name, schools=schools)


# Create a route for exporting CSV data
@main.route('/export_csv/<city_name>', methods=['POST'])
def export_csv(city_name):
    # Get the list of schools based on the city name
    schools = g_search(city_name)
    schools = schools[:maxSchdisplay]

    # Define the filename for the CSV file
    filename = f'{city_name}_schools.csv'

    # Generate CSV data by joining the list of schools with newline characters
    csv_data = '\n'.join(schools)

    # Create a Flask Response object with the CSV data and appropriate headers
    response = Response(csv_data, mimetype='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'

    # Return the response for triggering a file download
    return response


# Run the Flask application if this script is the main program
if __name__ == '__main__':
    main.run(debug=True)