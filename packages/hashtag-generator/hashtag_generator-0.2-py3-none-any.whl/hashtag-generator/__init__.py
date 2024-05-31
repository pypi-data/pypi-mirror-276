import os
import sys
import dotenv

current_directory = os.getcwd()
sys.path.append(current_directory)

dotenv.load_dotenv()
