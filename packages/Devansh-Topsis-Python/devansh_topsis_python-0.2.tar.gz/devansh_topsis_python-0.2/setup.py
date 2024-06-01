from setuptools import setup, find_packages

setup(
    name ="Devansh_Topsis_Python",
    version ="0.2",
    packages = find_packages(),
    author="Devansh Gupta",
    author_email="guptadevanshof2003@gmail.com",
    entry_points={
        "console_scripts": [
            "Topsis_Package=Topsis_Python.__init__:main"]},
    install_requires = [
        # python = 3.11.3
    ],
)