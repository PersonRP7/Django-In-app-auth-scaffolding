import sys
sys.path.append("..")
from unittest import main, TestCase
from test_auth import redirect, redirect_w_args
from auth import declare_auth_user_model_in_settings
from contextlib import redirect_stderr, redirect_stdout
import pathlib
import shutil
from functools import wraps

class SetupDir:

    root_name = ""
    app_name = ""

    # def create_app(self, app):#Shouldn't this be a directory?
    #     pathlib.Path(
    #         f"./{app}"
    #     ).touch()
    #     self.app_name += app
    #     return app

    def create_app(self, app):
        pathlib.Path(
            f"./{app}"
        ).mkdir(
            parents = True,
            exist_ok = True
        )
        self.app_name += app
        return app

    def create_root(self, root):
        pathlib.Path(
            f"./{root}"
        ).mkdir(
            parents = True,
            exist_ok = True
        )
        self.root_name += root
        return root

    def create_settings(self, callback):
        pathlib.Path(
            f"./{callback}/settings.py"
        ).touch()

    def destroy_root(self):
        shutil.rmtree(self.root_name)
        shutil.rmtree(self.app_name)

class TestDeclareAuthModel(TestCase, SetupDir):

    def setUp(self):
        self.create_app("one")
        self.create_settings(self.create_root("rdir"))

    def test_auth_user_model_declared_in_settings(self):
        response = declare_auth_user_model_in_settings(self.root_name, self.app_name)
        self.assertTrue(
            response
        )

    def test_auth_model_stdout(self):
        response = redirect_w_args(redirect_stdout, declare_auth_user_model_in_settings, self.root_name, self.app_name)
        self.assertEqual(
            response,
            "Declared AUTH_USER_MODEL in settings.py."
        )

    def tearDown(self):
        self.destroy_root()

class TestMissingSettings(TestCase, SetupDir):

    def test_no_model_in_root(self):
        response = declare_auth_user_model_in_settings("wrong_dir", "wrong_app")
        self.assertEqual(
            response,
            False
        )

    def test_no_model_stderr(self):
        response = redirect_w_args(redirect_stderr, declare_auth_user_model_in_settings, "wrong_dir", "wrong_app")
        self.assertEqual(
            response,
            "Couldn't locate settings.py"
        )

if __name__ == "__main__":
    main()
