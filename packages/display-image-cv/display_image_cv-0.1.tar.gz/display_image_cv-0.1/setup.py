from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    description = f.read()

setup(
    name="display_image_cv",
    version = '0.1',
    packages=find_packages(),
    install_requies = [
        "numpy",
        "os",
        "opencv-python",
    ],
    entry_points = {
        "console_scripts" : [
            "display_image_cv = display_image_cv:display_image",
        ],
    },
    long_description=description,
    long_description_content_type='text/markdown',
)