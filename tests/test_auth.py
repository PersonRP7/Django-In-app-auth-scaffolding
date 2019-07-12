import sys
sys.path.append("..")
from unittest import main, mock, TestCase
# from unittest.mock import patch
import auth
from contextlib import redirect_stdout, redirect_stderr
from contextlib import contextmanager
from io import StringIO
import pathlib
import shutil
import functools

@contextmanager
def mock_input(mock):
    original_input = __builtins__.input
    __builtins__.input = lambda _:mock
    yield
    __builtins__.input = original_input

def redirect(std_type, function):
    io_object = StringIO()
    with std_type(io_object):
        function()
    string = io_object.getvalue()
    return string

def redirect_w_args(std_type, function, *args):
    io_object = StringIO()
    with std_type(io_object):
        function(*args)
    string = io_object.getvalue()
    return string

def redirect_decorator(func):
    @functools.wraps(func)
    def wrapper(*args):
        return func(*args)
    return wrapper

class TestSimpleStdOut(TestCase):

    def test_warning_stdout(self):
        response = redirect(redirect_stdout, auth.warning)
        self.assertEqual(
            response,
"""Warning! Run this script against a fresh
django project as there could be data loss!"""
        )

    def test_exiting_stdout(self):
        response = redirect(redirect_stderr, auth.exiting)
        self.assertEqual(
            response,
            "Exiting."
        )

class TestDefaultAppAndRoot(TestCase):

    def test_root_name_default_empty(self):
        self.assertEqual(
            auth.root_name,
            ""
        )

    def test_app_name_default_empty(self):
        self.assertEqual(
            auth.app_name,
            ""
        )


# class TestRootAppSetters(TestCase):
#
#     def test_set_root_root(self):
#         with mock_input("root"):
#             self.assertEqual(
#                 auth.set_root_name(),
#                 "root"
#             )
#
#     def test_set_app_one(self):
#         with mock_input("one"):
#             self.assertEqual(
#                 auth.set_app_name(),
#                 "one"
#             )
class TestRootAppSetters(TestCase):
#Also works with "auth.input, here and through runner.py"
    def test_set_root_root(self):#This works.
        with mock.patch('builtins.input', return_value = "root"):
            self.assertEqual(
                auth.set_root_name(),
                "root"
            )

    def test_set_app_one(self):
        with mock.patch('builtins.input', return_value = "one"):
            self.assertEqual(
                auth.set_app_name(),
                "one"
            )

class TestAppReachable(TestCase):

    root = ""
    app = ""

    def structure_creator(self, *args):
        for i in args:
            pathlib.Path(
                f"./{i}"
            ).mkdir(
                parents = True,
                exist_ok = True
            )
        self.root += args[0]
        self.app += args[1]

    def setUp(self):
        self.structure_creator("rdir", "one")


    def test_app_reachable(self):
        response = auth.see_if_app_reachable(self.root, self.app)
        self.assertEqual(
            response,
            True
        )

    def test_reachable_wrong_root(self):
        response = auth.see_if_app_reachable("wrong_root", self.app)
        self.assertEqual(
            response,
            False
        )

    def test_reachable_wrong_app(self):
        response = auth.see_if_app_reachable(self.root, "wrong_app")
        self.assertEqual(
            response,
            False
        )

    def test_reachable_both_incorrect(self):
        response = auth.see_if_app_reachable("wrong_root", "wrong_app")
        self.assertEqual(
            response,
            False
        )

    def test_app_not_reachable_wrong_root_stderr(self):
        response = redirect_w_args(redirect_stderr, auth.see_if_app_reachable, "wrong_root", self.app)
        self.assertEqual(
            response,
            "Cannot reach the app."
        )

    def test_app_not_reachable_wrong_app_stderr(self):
        response = redirect_w_args(redirect_stderr, auth.see_if_app_reachable, self.root, "wrong_app")
        self.assertEqual(
            response,
            "Cannot reach the app."
        )

    def test_app_not_reachable_both_wrong_stderr(self):
        response = redirect_w_args(redirect_stderr, auth.see_if_app_reachable, "wrong_root", "wrong_app")
        self.assertEqual(
            response,
            "Cannot reach the app."
        )


    def tearDown(self):
        for i in [self.root, self.app]:
            shutil.rmtree(i)


if __name__ == "__main__":
    main()
