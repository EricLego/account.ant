from flask import Flask
from app.routes.ui_mock_routes import ui_mock_bp

app = Flask(__name__)
app.config["MOCK_MODE"] = True  # Enable mock mode

# Register blueprint without a prefix so routes like '/login' are accessible directly.
app.register_blueprint(ui_mock_bp)

if __name__ == "__main__":
    app.run(debug=True)
