import helpers
helpers.modify_system_path()


from apis import twilio
import unittest
# import time

class TestSendgrid(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSendgrid, self).__init__(*args, **kwargs)

    def test_can_import_sendgrid(self, *args, **kwargs):
        # from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        self.assertNotEqual(str(Mail).find('Mail'), -1)

    def test_can_import_sendgrid_api_module(self, *args, **kwargs):
        self.assertNotEqual(str(twilio.send_mail).find('function send_mail'), -1)

if __name__ == '__main__':
    unittest.main()


