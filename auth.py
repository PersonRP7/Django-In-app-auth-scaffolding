import os
import sys
import pathlib
import pdb

root_name = ""
app_name = ""

def warning():
    sys.stdout.write(
"""Warning! Run this script against a fresh
django project as there could be data loss!"""
    )

def ask_proceed():
    proceed = str(input("\nPress y to continue, anything else to cancel: "))
    yes = ['y' 'Y']
    for y in yes:
        if proceed in y:
            return True
        else:
            return False

def exiting():
    sys.stderr.write(
        "Exiting."
    )
    return False

def set_root_name():
    root_input = str(input("root name? "))
    global root_name
    root_name += root_input
    return root_input

def set_app_name():
    app_input = str(input("app name? "))
    global app_name
    app_name += app_input
    return app_input

def see_if_app_reachable(root_name, app_name):
    try:
        os.listdir(f"./{root_name}")
        os.listdir(f"./{app_name}")
        return True
    except FileNotFoundError:
        sys.stderr.write(
            "Cannot reach the app."
        )
        return False

def see_if_models_exists_in_app(app_name):
    try:
        if 'models.py' in os.listdir(f"./{app_name}"):
            return True
        else:
            sys.stderr.write(
                "Couldn't locate models.py"
            )
            return False
    except FileNotFoundError:
        sys.stderr.write(
            "Couldn't locate models.py"
        )
        return False

def declare_auth_user_model_in_settings(root_name, app_name):
    try:
        with open(f"./{root_name}/settings.py", "a") as outbound:
            outbound.write(
f"""AUTH_USER_MODEL = '{app_name}.CustomUser'"""
            )
            sys.stdout.write(
                f"Declared AUTH_USER_MODEL in settings.py."
            )
            return True
    except FileNotFoundError:
        sys.stderr.write(
            "Couldn't locate settings.py"
        )
        return False

def create_py_file_from_txt_file(app, txt_file, py_file):
    try:
        with open(f"./py_files/{txt_file}") as inbound:
            data = inbound.read()
            with open(f"./{app}/{py_file}", "w") as file:
                file.write(data)
                return True
    except FileNotFoundError:
        sys.stderr.write("Cannot find the app or the base txt file.")
        return False


def program_runner():
    warning()
    if ask_proceed():
        set_root_name()
        set_app_name()
        see_if_app_reachable(root_name, app_name)
        see_if_models_exists_in_app(app_name)
        declare_auth_user_model_in_settings(root_name, app_name)
        create_py_file_from_txt_file(app_name, "forms.txt", "forms.py")
        create_py_file_from_txt_file(app_name, "admin.txt", "admin.py")
        create_py_file_from_txt_file(app_name, "custom_user.txt", "models.py")
    else:
        exiting()

if __name__ == "__main__":
    program_runner()
