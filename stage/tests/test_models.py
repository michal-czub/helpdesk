from django.test import TestCase
from helpdesk import settings
from stage.models import Stage
from board.models import Board
from project.models import Project

class StageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_project = Project.objects.create(name="test_project")
        test_board = Board.objects.create(name="test_board", project=test_project)
        Stage.objects.create(name="test_name", order=0, board=test_board)

    def test_stage_model_is_configured(self):
        assert "stage" in settings.INSTALLED_APPS

    def test_string_method(self):
        stage = Stage.objects.first()
        self.assertEqual(stage.__str__(), "test_name")

    def test_get_name_method(self):
        stage = Stage.objects.first()
        self.assertEqual(stage.get_name(), "test_name")

    def test_get_details_method(self):
        stage = Stage.objects.first()
        self.assertEqual(stage.get_details()["id"], stage.id)
        self.assertEqual(stage.get_details()["name"], stage.name)
        self.assertEqual(stage.get_details()["order"], stage.order)

    def test_pre_save_order_method(self):
        pass
