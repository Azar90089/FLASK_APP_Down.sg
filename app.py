from flask import Flask, request, render_template
import requests
import time

app = Flask(__name__)

# Home page
@app.route('/', methods=['GET', 'POST'])
def home():
    status = None
    url = None
    response_time = None
    error = None
    status_code = None
    
    if request.method == 'POST':
        url = request.form.get('url')
        if not url.startswith('http://') and not url.startswith('https://'):
            url = f'http://{url}'

        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)
            end_time = time.time()
            response_time = round((end_time - start_time) * 1000, 2)  # in ms
            status_code = response.status_code
            status = 'Up' if response.status_code == 200 else 'Issues'
        except requests.exceptions.RequestException as e:
            status = 'Down'
            error = str(e)

    return render_template(
        'index.html',
        url=url,
        status=status,
        response_time=response_time,
        status_code=status_code,
        error=error
    )

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
