# handle attachment files, save and return the list of attachment files

from werkzeug.utils import secure_filename
from fastapi import File, UploadFile

import os
import shutil

# def upload_file()
