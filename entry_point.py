import sys
# from create_test_users import create_test_users

from mpgame.Controller.factory import create_app

sio, app = create_app()

if __name__ == '__main__':
    # if '--create-test-users' in sys.argv or \
    #     '--test' in sys.argv or \
    #     '-t' in sys.argv:
    #         create_test_users(app)
    sio.run(app, debug=False, host='0.0.0.0')