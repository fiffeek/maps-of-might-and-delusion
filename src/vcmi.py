from typing import Optional
from docker import DockerClient
from docker.types import Mount

from logger import logger


class VCMI:
    def __init__(
        self,
        repository: str,
        tag: str,
        docker_client: DockerClient,
        display: int,
        homm_data_path: str,
        xauth_mount_dir: str,
        name: Optional[str] = None,
    ) -> None:
        self.repository = repository
        self.tag = tag
        self.image = f"{repository}:{tag}"
        self.client = docker_client
        self.display = display
        self.container = None
        self.name = name
        self.homm_data_path = homm_data_path
        self.xauth_mount_dir = xauth_mount_dir

    def start(self):
        data_mount = "/mnt/homm/data"
        xauth_mount = "/mnt/xauth/data"
        self.container = self.client.containers.run(
            self.image,
            detach=True,
            environment={
                "DISPLAY_NUM": f"{self.display}",
                "HOMM_DATA_PATH": data_mount,
                "XAUTH_DIR": xauth_mount,
                "SCREEN_W": "1600",
                "SCREEN_H": "1080",
            },
            name=self.name,
            init=True,
            remove=True,
            mounts=[
                Mount(
                    source=self.homm_data_path,
                    target=data_mount,
                    type="bind",
                    read_only=True,
                ),
                Mount(
                    source=self.xauth_mount_dir,
                    target=xauth_mount,
                    type="bind",
                ),
            ],
            # TODO configuration
            ports={
                "5900/tcp": ("127.0.0.1", 5900),
                f"{self.exposed_port}/tcp": ("127.0.0.1", self.exposed_port),
            },
        )

    @property
    def xauth_file(self):
        return f"{self.xauth_mount_dir}/.Xauthority"

    @property
    def local_display(self):
        return self.display

    @property
    def exposed_port(self):
        return 6000 + self.display

    def stream_logs(self):
        """
        Blocks on logs reading.
        """
        if self.container is None:
            raise RuntimeError("vcmi container has not been started")
        for log in self.container.logs(stream=True, follow=True):
            logger.debug(str(log))

    def stop(self):
        if self.container:
            self.container.stop()

    def maximize(self):
        command = f'DISPLAY=:{self.display} wmctrl -r "VCMI Map Editor" -b add,maximized_vert,maximized_horz'
        self.run_command(command)

    def run_command(self, command: str):
        logger.debug(f"Running command: {command}")
        if self.container is None:
            raise RuntimeError("vcmi container has not been started")
        result = self.container.exec_run(["/bin/sh", "-lc", command])
        if result.exit_code != 0:
            raise RuntimeError(
                f"cant run the command in the container, out: {result.output}"
            )
        logger.debug(result.output)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
