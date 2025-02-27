from flask import Flask
from flask_cors import CORS
from app.routes.ui_mock_routes import ui_mock_bp

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from React

# Register blueprint so endpoints match the ones in your React code
app.register_blueprint(ui_mock_bp)

if __name__ == "__main__":
    app.run(debug=True)
