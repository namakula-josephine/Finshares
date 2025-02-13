from app.routes import main
app.register_blueprint(main)


from flask import Flask, render_template

# Initialize Flask app
app = Flask(__name__)

# Route for the homepage
@app.route('/')
def home():
    return '<h1>Welcome to FinShares</h1>'

# Route for the register page
@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
