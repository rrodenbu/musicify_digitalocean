##################################################
# Sensitive Settings
##################################################

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$gy5cj46_&4ba$2nbe43ikp2qe^8ls2u32fv%-bbyusyr0pm#p'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'musicify',
        'USER': 'root',
        'PASSWORD': 'rootroot',
        'HOST': 'webapp.corwalcoocbk.us-east-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}

# Real email sending behavior can be achieve by uncomment and config the following
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'musicify.t254@gmail.com'
EMAIL_HOST_PASSWORD = 'judynguyenriley'

#twiliio: messaging api
TWILIO_ACCOUNT_SID = 'AC170cc7a17ad1ccc209c3c6cb063d4248'
TWILIO_API_KEY = 'SK674996a333385b05da46111819461838'
TWILIO_API_SECRET = 'I7hRwzY9TWU7lB9ozcDg3GXI7fySjjxJ'
TWILIO_IPM_SERVICE_SID = 'IS1a72a412340b47a3aa99f27b874a3c67'
TWILIO_AUTH_TOKEN = '3f62b444d36ceb130ab7a0f3d87c1ce3'#https://www.twilio.com/console

# Spotify credentials
CLIENT_ID = '71a83ef9fa6d4429a9336363738b5b0a'
CLIENT_SCERECT = '1700c3890fcc4b868981c270da4873d8'
