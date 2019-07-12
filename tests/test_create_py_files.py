import sys
import os
sys.path.append("..")
from unittest import mock, main, TestCase
from unittest.mock import mock_open
from test_auth import redirect_w_args
from auth import create_py_file_from_txt_file
from contextlib import redirect_stderr
import pathlib
import shutil


class TestCreatepyFiles(TestCase):

    app_name = ""

    def create_app_and_py_files(self,name):
        dirs = ['py_files']
        dirs.append(name)
        for i in dirs:
            pathlib.Path(
                f"./{i}"
            ).mkdir(
                parents = True,
                exist_ok = True
            )
        self.app_name += name

    def put_txt_file_in_py_files(self, name):
        pathlib.Path(
            f"./py_files/{name}"
        ).touch()

    def put_txt_into_txt_file_in_py_files(self, file_):
        with open(f"./py_files/{file_}", "w") as file:
            file.write("gibberish text")

    def destroy_dirs(self):
        dirs = [self.app_name, 'py_files']
        for dir in dirs:
            shutil.rmtree(dir)

    def setUp(self):
        self.create_app_and_py_files("one")
        self.put_txt_file_in_py_files("custom_user.txt")
        self.put_txt_into_txt_file_in_py_files("custom_user.txt")


    def test_writes_from_py_files_to_app(self):
        response = create_py_file_from_txt_file(
            self.app_name, "custom_user.txt", "models.py"
        )
        self.assertTrue(response)

    def tearDown(self):
        self.destroy_dirs()


class TestCreatepyFilesError(TestCase):

    def test_error(self):
        response = create_py_file_from_txt_file(
            "wrong_app", "wrong_txt_file", "wrong_py_file"
        )
        self.assertFalse(response)

    def test_error_stderr(self):
        response = redirect_w_args(
            redirect_stderr,
            create_py_file_from_txt_file,
            "wrong_app",
            "wrong_txt_file",
            "wrong_py_file"
        )
        self.assertEqual(
            response,
            "Cannot find the app or the base txt file."
        )



if __name__ == "__main__":
    main()
