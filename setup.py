from setuptools import setup, find_packages


setup(name='pt-regions',
      version='1.0.0',
      author='Jorge C. Leitão',
      author_email='jorgecarleitao@gmail.com',
      packages=find_packages(),
      license='MIT',
      package_data={'pt_regions': ['raw_data/*', 'municipalities.json',
                                   'counties.json']},
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Topic :: Utilities',
      ],
)
