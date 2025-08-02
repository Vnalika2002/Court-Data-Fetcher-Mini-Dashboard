from flask import Flask, render_template, request, send_file, flash
from scraper import fetch_case_details
from models import init_db, log_query
import os

app = Flask(__name__)
app.secret_key = 'your_secret'  # move to env variable for production

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        case_type = request.form['case_type']
        case_number = request.form['case_number']
        filing_year = request.form['filing_year']

        try:
            html, parsed = fetch_case_details(case_type, case_number, filing_year)
            log_query(case_type, case_number, filing_year, html)
            if parsed.get('error'):
                flash(parsed['error'], 'danger')
                return render_template('index.html')
            return render_template('result.html', data=parsed)
        except Exception as e:
            flash(f"Internal error: {str(e)}", 'danger')
            return render_template('index.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
