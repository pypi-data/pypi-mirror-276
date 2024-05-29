from setuptools import setup, find_packages

import distutils.command.build

# Override build command
class BuildCommand(distutils.command.build.build):
    def initialize_options(self):
        distutils.command.build.build.initialize_options(self)
        self.build_base = '.build'

setup(
    cmdclass={"build": BuildCommand},
    name='ezhub',
    version='0.1.0',
    author='0to1toeverything',
    packages=find_packages(),
    install_requires=[
        # 你的项目依赖的库
    ],
    # entry_points={
    #     'console_scripts': [
    #         'winbuild = om_tools.winbuild.winbuild_client:main',
    #         'winby = om_tools.winbuild.winbuild_cmd:kk',
    #     ],
    # }
)
