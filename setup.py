

from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()


def install_requirements():
    return [package_string.strip() for package_string in open('requirements.txt', 'r')]


setup(name='ssspend',
      version="0.0.1",
      description="SS Spending Tools",
      long_description="Spending Tools on Google Sheet",
      classifiers=[
          "Topic :: Office/Business :: Financial :: Accounting",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "License :: OSI Approved :: MIT License",
      ],
      keywords="SS Spend Google Sheet Spreadsheet",
      url="https://github.com/stephenhky/SSSpend",
      author="Kwan-Yuet Ho",
      author_email="stephenhky@yahoo.com.hk",
      license='MIT',
      packages=['ssspend',],
      # package_data={},
      setup_requires=[],
      install_requires=install_requirements(),
      tests_require=[
          'unittest2',
      ],
      include_package_data=True,
      test_suite="test",
      zip_safe=False)

