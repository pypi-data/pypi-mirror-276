from setuptools import setup, find_packages

setup(
    name='id_card_recognition',
    version='0.3.5',
    packages=find_packages(),
    install_requires=[
        'requests',
        'natsort',
        'openai',
        'python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'id_card_recognition = id_card_recognition.recognition:main',
        ],
    },
    author='freedak Wang',
    author_email='freedak@163.com',
    description='A package for ID card recognition using OpenAI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/freedak-wang/id_card_recognition',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
