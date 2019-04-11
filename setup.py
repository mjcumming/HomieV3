import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(name='Homie3',
      version='0.0.2',
      description='Homie 3.0.1 Implementation',
      author='Michael Cumming',
      author_email='mike@4831.com',
      long_description=long_description,
      long_description_content_type="text/markdown",      
      url='https://github.com/mjcumming/Homie',
      packages=setuptools.find_packages(),
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],      
)
