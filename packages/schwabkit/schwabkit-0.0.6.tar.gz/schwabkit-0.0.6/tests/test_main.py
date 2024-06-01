import schwabkit
import dotenv
import os

dotenv.load_dotenv()

asd = schwabkit.Client(os.getenv('app_key'), os.getenv('app_secret'), os.getenv('callback_url'))
asd.update_tokens_auto()


