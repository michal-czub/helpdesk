from django.test import TestCase
from helpdesk import settings
from team.models import Team

class TeamModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Team.objects.create(name="Testowy")

    def test_team_model_is_configured(self):
        assert "team" in settings.INSTALLED_APPS

    def test_string_method(self):
        team = Team.objects.first()
        expected = f"{team.name}"
        self.assertEqual(str(team.name), expected)

    def test_string_method_2(self):
        team = Team.objects.first()
        self.assertEqual(team.__str__(), team.name)

    def test_get_details(self):
        team = Team.objects.first()
        expected = f"'id': '{team.id}' 'name': '{team.name}'"
        self.assertEqual(team.get_details()["id"], team.id)
        self.assertEqual(team.get_details()["name"], team.name)


# import pytest
# from helpdesk import settings
# from team.models import Team
#
# def test_example():
#     assert 1 == 1
#
# class TestCreateTeam:
#     def test_team_model_is_configured(self):
#         assert "team" in settings.INSTALLED_APPS
#
#     @pytest.mark.django_db
#     def test_create_team(self, db) -> None:
#         Team.objects.create(name="Zespol A")
#         assert Team.objects.count() == 1
#
#     def test_get_details(self):

