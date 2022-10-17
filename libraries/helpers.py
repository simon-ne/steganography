import os

def remove_all_from_dir(dir_path):
    for f in os.listdir(dir_path):
        os.remove(os.path.join(dir_path, f))


def errors_add(errors_dict, error_type, error):
    try:
        errors_dict[error_type]
    except:
        errors_dict[error_type] = []
    
    errors_dict[error_type].append(error)
    return errors_dict


def validate_input_encode(form, files):
    errors = {}

    try:
        message = form["message"]
        if message == "":
            errors_add(errors, "message", "Message can't be empty when encoding.")
    except:
        errors_add(errors, "message", "Message can't be empty when encoding.")

    try:
        image = files["image"]
        if image.filename == "":
            errors_add(errors, "image", "Image must be selected.")
    except:
        errors_add(errors, "image", "Image must be selected.")
    
    if image.filename.split(".")[-1] != "png":
        errors_add(errors, "image", "Only PNG images are supported.")

    validity = True if errors == {} else False
    return validity, errors


def validate_input_decode(files):
    errors = {}

    try:
        image = files["image"]
        if image.filename == "":
            errors_add(errors, "image", "Image must be selected.")
    except:
        errors_add(errors, "image", "Image must be selected.")
    
    if image.filename.split(".")[-1] != "png":
        errors_add(errors, "image", "Only PNG images are supported.")

    validity = True if errors == {} else False
    return validity, errors