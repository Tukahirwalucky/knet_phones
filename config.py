class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/knet-phones'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    JWT_SECRET_KEY = '12345'  # Ensure this is the same as in your JWT initialization
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    MAIL_SERVER = 'smtp.example.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'kojashraf@gmail.com'
    MAIL_PASSWORD = 'Ashraf@001'
    MAIL_DEFAULT_SENDER = 'your-email@exaz zmple.com'
