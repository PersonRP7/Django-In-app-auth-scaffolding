import sys
sys.path.append("..")
import auth
from unittest import TestCase, main, mock


class TestProceed(TestCase):

   @mock.patch('auth.input', create = True)
   def test_proceed_true(self, mocked_input):
       mocked_input.side_effect = ['y', 'Y']
       response = auth.ask_proceed()
       self.assertEqual(
           response,
           True
       )

   @mock.patch('auth.input', create = True)
   def test_proceed_false(self, mocked_input):
       mocked_input.side_effect = ['n']
       response = auth.ask_proceed()
       self.assertEqual(
            response,
            False
       )

if __name__ == "__main__":
    main()
