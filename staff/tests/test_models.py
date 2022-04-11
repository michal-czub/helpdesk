from django.test import TestCase
from helpdesk import settings
from staff.models import Staff


class StaffModelTest(TestCase):
    def test_staff_model_is_configured(self):
        assert "staff" in settings.INSTALLED_APPS

    def test_create_user_method_correct(self):
        user = Staff.objects.create_user(phone_number='+48609500500', password='test_password',
                                         name="test_name", email="test@mail.com")
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_create_super_user_method_correct(self):
        user = Staff.objects.create_superuser(phone_number='+48609500500', password='test_password',
                                         name="test_name", email="test@mail.com")
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_raise_value_error_for_phone_number(self):
        with self.assertRaises(ValueError):
            Staff.objects.create_user(password='test_password',
                                      phone_number='',
                                      name="test_name",
                                      email="test@mail.com")

    def test_raise_value_error_for_password(self):
        with self.assertRaises(ValueError):
            Staff.objects.create_user(password="",
                                      phone_number="+48609500500",
                                      name="test_name",
                                      email="test@mail.com")

    def test_str_method(self):
        staff = Staff.objects.create_user(password="test_password",
                                  phone_number="+48609500500",
                                  name="test_name",
                                  email="test@mail.com")
        self.assertEqual(staff.__str__(), "test_name")

    def test_get_name_method(self):
        staff = Staff.objects.create_user(password="test_password",
                                  phone_number="+48609500500",
                                  name="test_name",
                                  email="test@mail.com")
        self.assertEqual(staff.get_name(), "test_name")

    def test_get_email_method(self):
        staff = Staff.objects.create_user(password="test_password",
                                  phone_number="+48609500500",
                                  name="test_name",
                                  email="test@mail.com")
        self.assertEqual(staff.get_email(), "test@mail.com")

    def test_get_details(self):
        staff = Staff.objects.create_user(password="test_password",
                                  phone_number="+48609500500",
                                  name="test_name",
                                  email="test@mail.com")
        self.assertEqual(staff.get_details()["name"], staff.name)
        self.assertEqual(staff.get_details()["email"], staff.email)
        self.assertEqual(staff.get_details()["id"], staff.id)
        self.assertEqual(staff.get_details()["is_active"], staff.is_active)
        self.assertEqual(staff.get_details()["is_staff"], staff.is_staff)
        self.assertEqual(staff.get_details()["is_admin"], staff.is_admin)

    def test_has_perm_method(self):
        staff = Staff.objects.create_superuser(password="test_password",
                                  phone_number="+48609500500",
                                  name="test_name",
                                  email="test@mail.com")
        self.assertTrue(staff.has_perm(staff.is_admin), staff.is_admin)

    def test_has_module_perms(self):
        staff = Staff.objects.create_superuser(password="test_password",
                                  phone_number="+48609500500",
                                  name="test_name",
                                  email="test@mail.com")
        self.assertTrue(staff.has_module_perms(staff.is_admin), staff.is_admin)

    def test_property_is_active(self):
        staff = Staff.objects.create_user(password="test_password", phone_number="+48609500500",
                                          name="test_name", email="test@mail.com")
        self.assertEqual(staff.f_is_active, True)

    def test_property_is_staff(self):
        staff = Staff.objects.create_superuser(password="test_password", phone_number="+48609500500",
                                               name="test_name", email="test@mail.com")
        self.assertEqual(staff.f_is_staff, True)

    def test_property_is_admin(self):
        staff = Staff.objects.create_superuser(password="test_password", phone_number="+48609500500",
                                               name="test_name", email="test@mail.com")
        self.assertEqual(staff.f_is_admin, True)
