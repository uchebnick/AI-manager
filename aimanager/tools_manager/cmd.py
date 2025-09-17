from setuptools import setup, find_packages

setup(
    name="aimanager",
    version="0.1.0",
    description="Менеджер инструментов",
    packages=find_packages(),
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'aimanager-cli = aimanager.tools_manager.router',
        ],
    },
)
