from setuptools import setup, find_packages

setup(
    name='connect_four_tobiasocula',
    version='1.0.5',  # Increment this version number
    description='Your package description',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/your-repo',
    packages=find_packages(),
    install_requires=[
        # Your dependencies
    ],
)