from mtodo import create_app, socketio


def main():
    app = create_app()
    socketio.run(app, debug=True)


if __name__ == "__main__":
    main()
