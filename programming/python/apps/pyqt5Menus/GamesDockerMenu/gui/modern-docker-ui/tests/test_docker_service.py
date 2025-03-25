import unittest
from src.services.docker_service import DockerService

class TestDockerService(unittest.TestCase):

    def setUp(self):
        self.docker_service = DockerService()

    def test_get_images(self):
        images = self.docker_service.get_images()
        self.assertIsInstance(images, list)

    def test_run_container(self):
        result = self.docker_service.run_container('nginx')
        self.assertTrue(result)

    def test_stop_container(self):
        self.docker_service.run_container('nginx')
        result = self.docker_service.stop_container('nginx')
        self.assertTrue(result)

    def test_remove_container(self):
        self.docker_service.run_container('nginx')
        result = self.docker_service.remove_container('nginx')
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()