import unittest
from src.models.docker import DockerImage, DockerContainer
from src.models.settings import AppSettings

class TestDockerImage(unittest.TestCase):
    def setUp(self):
        self.image = DockerImage(name="test_image", tag="latest")

    def test_image_creation(self):
        self.assertEqual(self.image.name, "test_image")
        self.assertEqual(self.image.tag, "latest")

    def test_image_full_name(self):
        self.assertEqual(self.image.full_name(), "test_image:latest")

class TestDockerContainer(unittest.TestCase):
    def setUp(self):
        self.container = DockerContainer(name="test_container", image="test_image:latest")

    def test_container_creation(self):
        self.assertEqual(self.container.name, "test_container")
        self.assertEqual(self.container.image, "test_image:latest")

    def test_container_start(self):
        self.container.start()
        self.assertTrue(self.container.is_running)

    def test_container_stop(self):
        self.container.start()
        self.container.stop()
        self.assertFalse(self.container.is_running)

class TestAppSettings(unittest.TestCase):
    def setUp(self):
        self.settings = AppSettings()

    def test_default_settings(self):
        self.assertIsNotNone(self.settings.load())

    def test_save_settings(self):
        self.settings.save({"key": "value"})
        self.assertEqual(self.settings.load().get("key"), "value")

if __name__ == '__main__':
    unittest.main()