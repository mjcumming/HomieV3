from setuptools import setup

install_requires = list(val.strip() for val in open('requirements.txt'))

setup(name='Homie3',
      version='0.0.1',
      description='Homie 3.0 Device Implementation',
      author='Michael Cumming',
      author_email='mike@4831.com',
      url='https://github.com/mjcumming/Homie',
      packages=['homie'],
      install_requires=install_requires,
)
