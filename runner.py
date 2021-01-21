from app import create_app

main_app = create_app()

application = main_app

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8899, debug=True)
