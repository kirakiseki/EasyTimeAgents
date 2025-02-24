import os
from . import CONFIG


def copy_upload_file(upload_data) -> str:
    if not upload_data or upload_data is None or upload_data == "":
        return "NO_UPLOAD_FILE"

    filename = upload_data.name
    upload_dir = CONFIG["file_upload_dir"]
    new_path = os.path.join(upload_dir, filename)

    with open(new_path, "wb") as f:
        f.write(upload_data.getvalue())

    return new_path
