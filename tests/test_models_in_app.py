import sys
sys.path.append("..")
from unittest import main, TestCase
from test_auth import mock_input, redirect, redirect_w_args
from auth import see_if_models_exists_in_app
from contextlib import redirect_stdout, redirect_stderr
import pathlib
import shutil

class DirCreator:

    app_name = ""

    @staticmethod
    def create_app(app):
        pathlib.Path(
            f"./{app}"
        ).mkdir(
            parents = True,
            exist_ok = True
        )
        pathlib.Path(
            f"./{app}/models.py"
        ).touch()
        return app

    @classmethod #create_app is the callback
    def set_app(cls, callback):
        cls.app_name += callback

    def app_deleter(self):
        shutil.rmtree(self.app_name)

class TestModelsInApp(TestCase, DirCreator):

    def setUp(self):#set_app gets its value from the return value of create_app
        DirCreator().set_app(DirCreator.create_app("new_app"))

    def test_returns_true_models_exists(self):
        response = see_if_models_exists_in_app(self.app_name)
        self.assertEqual(
            response,
            True
        )

    def tearDown(self):
        self.app_deleter()


class TestModelNotExistsInApp(TestCase, DirCreator):

    def setUp(self):
        DirCreator.create_app("one")

    def test_no_models_stderr(self):
        print(self.app_name)
        response = redirect_w_args(redirect_stderr, see_if_models_exists_in_app, self.app_name)
        self.assertEqual(
            response,
            "Couldn't locate models.py"
        )

    def tearDown(self):
        shutil.rmtree("one")

if __name__ == "__main__":
    main()
