from setuptools import setup
import os
import subprocess
from cmake_build_extension import BuildExtension, CMakeExtension

current_path = os.path.dirname(os.path.abspath(__file__))

# Required dependencies
REQUIRED_PACKAGES = [
    "setuptools>=61.0",
    "cmake>=3.30.4",
    "cmake_build_extension>=0.6.1",
]


class CustomBuildExtCommand(BuildExtension):
    def run(self):
        subprocess.run(["mkdir", "-p", "{current_path}/rdk_install"])

        # Run the custom shell commands
        subprocess.run(
            [
                "bash",
                "build_and_install_dependencies.sh",
                os.path.join(current_path, "rdk_install"),
            ],
            cwd=os.path.join(current_path, "thirdparty"),
        )
        # Call the original build_ext command
        print("calling super run")
        super().run()


setup(
    name="flexiv_rdk",
    packages=[],
    setup_requires=REQUIRED_PACKAGES,
    install_requires=REQUIRED_PACKAGES,
    python_requires=">=3.10.0",
    version="0.1",
    ext_modules=[
        CMakeExtension(
            name="flexiv_rdk",
            source_dir=current_path,
            cmake_configure_options=[
                f"-DCMAKE_INSTALL_PREFIX={current_path}/rdk_install",
                "-DINSTALL_PYTHON_RDK=ON",
            ],
        ),
    ],
    cmdclass={"build_ext": CustomBuildExtCommand},
)
