from flask_app import init_app

app = init_app()

# Start the server
if __name__ == "__main__":

    app.run_server(debug=True, host="0.0.0.0")
