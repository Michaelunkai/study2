class DockerImage:
    def __init__(self, name, tag, size):
        self.name = name
        self.tag = tag
        self.size = size

    def __repr__(self):
        return f"DockerImage(name={self.name}, tag={self.tag}, size={self.size})"


class DockerContainer:
    def __init__(self, container_id, image, status):
        self.container_id = container_id
        self.image = image
        self.status = status

    def __repr__(self):
        return f"DockerContainer(container_id={self.container_id}, image={self.image}, status={self.status})"