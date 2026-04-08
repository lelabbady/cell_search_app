from cell_search.app import create_dash_app
from cell_search.config import DEFAULT_HOST, DEFAULT_PORT


app = create_dash_app()

# Run the app
if __name__ == "__main__":
    app.run(host=DEFAULT_HOST, port=DEFAULT_PORT, debug=True)






