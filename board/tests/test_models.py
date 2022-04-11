from django.test import TestCase
from helpdesk import settings
from board.models import Board
from project.models import Project

class BoardModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        project = Project.objects.create(name="project")
        Board.objects.create(name="board", project=project)

    def test_board_model_is_configured(self):
        assert "board" in settings.INSTALLED_APPS

    def test_str_method(self):
        board = Board.objects.first()
        self.assertEqual(board.__str__(), "board")

    def test_get_details(self):
        board = Board.objects.first()
        self.assertEqual(board.get_details()["id"], board.id)
        self.assertEqual(board.get_details()["name"], "board")

    def test_get_project_details(self):
        board = Board.objects.first()
        self.assertEqual(board.get_project_details()["id"], board.project.id)
        self.assertEqual(board.get_project_details()["name"], board.project.name)
