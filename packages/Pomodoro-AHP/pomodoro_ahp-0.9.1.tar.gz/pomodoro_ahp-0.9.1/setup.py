from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="Pomodoro_AHP",
    version="0.9.1",
    description='CLI implementation of "Pomodoro Timer" written in Python',
    # py_modules=['files'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/you-know-wh0/Pomodoro-Timer-2",
    author="Prova, Rashid",
    author_email="zamiulrashid1@gmail.com, azrahumayraprova@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'Pomodoro_Timer = files.__main__:start'
        ]
    },
    python_requires=">=3.10",
    packages=find_packages(include=['Pomodoro_Timer', 'Pomodoro_Timer.*', 'files', 'files.*']),
    include_package_data=True,
    install_requires=[
        "pygame",
        "keyboard",
    ],
)
