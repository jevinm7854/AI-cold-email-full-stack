from flaskr.app import create_app
import os

app = create_app()

if __name__ == "__main__":

    PORT = os.getenv("PORT", 9000)
    app.run(debug=True, port=PORT)
