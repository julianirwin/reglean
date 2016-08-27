from setuptools import setup, find_packages

setup(name='reglean',
      version='0.0.0',
      description=u"Glean metadata from a filename",
      classifiers=[],
      keywords='re',
      author=u"Julian Irwin",
      author_email='julian.irwin@gmail.com',
      url='https://bitbucket.com/gradi3nt/reglean',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[],
      setup_requires=['nose>=1.0'],
      extras_require={
          'test': ['nose'],
      },
      test_suite = 'nose.collector',
      entry_points = {
          'console_scripts': [],
          }
      )
