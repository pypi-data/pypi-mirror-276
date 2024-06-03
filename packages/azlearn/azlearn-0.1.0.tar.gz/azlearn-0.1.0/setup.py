from setuptools import setup, find_packages

setup(
  name='azlearn',
  version='0.1.0',  # Start with version 0.1.0 for initial release
  packages=find_packages(where='azlearn'),  # Assuming your code is in the 'src' folder
  author='AnassKEMMOUNE ZakariaCHOUKRI',
  author_email='anasskemmoune03@gmail.com',
  description='This is a Lightweight complete package for machine learning projects.',
  long_description='This is a Lightweight complete package for machine learning projects.',
  long_description_content_type='text/markdown',  # If using Markdown for long description
  url='https://github.com/zakariaCHOUKRI/azlearn/',  # Link to your repository (optional)
  install_requires=[  # List of dependencies your package needs
      'numpy',
      'scikit-learn',
  ],
  classifiers=[  # Classify your package (optional)
      'Programming Language :: Python :: 3',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
  ],
)