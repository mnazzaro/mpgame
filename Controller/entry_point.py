from factory import create_app

if __name__ == '__main__':
    # game_id = os.environ.get('GAME_ID') # This may come in an argument or env var - I don't know yet
    app = create_app()
    app.run(debug=False)