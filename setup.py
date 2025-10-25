import os.path
import shutil

from setuptools import Command, setup
from setuptools.command.build import build


class build_client(Command):
    def initialize_options(self) -> None:
        self.client_dir = None
        self.editable_mode = False

    def finalize_options(self) -> None:
        bdist_dir = self.get_finalized_command("bdist_wheel").bdist_dir

        if bdist_dir:
            self.client_dir = os.path.join(bdist_dir, "zundamahjong", "client")

    def run(self) -> None:
        """Build the Zundamahjong static client files."""

        if self.editable_mode:
            return

        if not os.path.isdir("client_build"):
            os.chdir("client")

            self.spawn(["npm", "install"])
            self.spawn(["npm", "run", "build"])

            os.chdir("..")

        if self.client_dir:
            shutil.copytree("client_build", self.client_dir)


class custom_build(build):
    sub_commands = [("build_client", None)] + build.sub_commands


setup(
    cmdclass={
        "build_client": build_client,
        "build": custom_build,
    },
)
