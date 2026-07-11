from backend.app import create_app
from backend.config import HOST, PORT


def main() -> None:
    app = create_app()
    app.run(host=HOST, port=PORT, debug=True)


if __name__ == "__main__":
    main()
