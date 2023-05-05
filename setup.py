from setuptools import setup

setup(
    name='mpgame',
    version='0.1.0',    
    description='The core game service library for Metal Poker',
    url='https://github.com/mnazzaro/mpgame',
    author='Mark Nazzaro',
    author_email='marknazzaro2@gmail.com',
    license='BSD 2-clause',
    packages=['mpgame'],
    install_requires=['celery==5.2.7',
                      'Flask==2.2.2',
                      'Flask_Cors==3.0.10',
                      'Flask_Login==0.6.2',
                      'Flask_SocketIO==5.3.2',
                      'mplib==0.1.0',
                      'pokerface==1.0.2',
                      'Requests==2.30.0'
                    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: None',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',       
        'Programming Language :: Python :: 3.9'
    ],
)