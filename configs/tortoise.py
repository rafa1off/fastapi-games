import os
from dotenv import load_dotenv
load_dotenv()

TORTOISE_ORM = {
    'connections': {
        'default': os.getenv('POSTGRES_URL')
    },
    'apps': {
        'models': {
            'models': [
                'models.games',
                'aerich.models'
            ],
        }
    }
}
