from app.models import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)  # Ensure debug mode is enabled for detailed error messages
