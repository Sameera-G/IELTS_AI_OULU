from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Route for handling the "Reading" button click
@app.route('/reading', methods=['GET'])
def reading():
    # Here, you can perform any necessary operations before rendering the template
    # For example, you can pass parameters to the template or process data
    
    # Redirect to the main page with the selected role as a query parameter
    # For demonstration, let's assume the selected role is "Reading"
    return redirect(url_for('main', selected_role='Reading'))

# Route for handling navigation from the second page to the third page
@app.route('/next_page', methods=['GET'])
def next_page():
    # Redirect to the route that renders the third page
    return redirect(url_for('third_page'))

# Route for rendering the third page
@app.route('/third_page', methods=['GET'])
def third_page():
    # Render the third_page.html template
    return render_template('third_page.html')

# Route for rendering the main page with the selected role
@app.route('/<selected_role>', methods=['GET'])
def main(selected_role):
    return render_template('reading_page.html', selected_role=selected_role)

if __name__ == '__main__':
    app.run(debug=True)
