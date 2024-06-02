import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'uwrapper',
    packages=setuptools.find_packages(),
    version = '0.0.7',
    include_package_data=True,
    description = 'Python library for upstox APIs',
    long_description=long_description,
    long_description_content_type="text/markdown",  author = 'Zachbot',
    author_email = 'zachbot006@gmail.com',
    url = 'https://github.com/azachbot/upstox_api_wrapper',
    install_requires=['requests', 'pandas','upstox-python-sdk'],
    keywords = ['upstox', 'nse', 'python', 'sdk', 'trading', 'stock markets', 'wrapper'],
    classifiers=[
      'Intended Audience :: Developers',
      'Natural Language :: English',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: Implementation :: PyPy',
      'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)