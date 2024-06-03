from setuptools import setup, find_packages

with open('Readme.md', 'r') as f:
    long_description = f.read()

setup(
    name='pulse_linter',
    version='0.0.5',
    description='Security Weakness Finder',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='sooraj',
    author_email='sooraj.cs22@duk.ac.in',
    license='Nil',
    packages=find_packages(),
    install_requires=[
        'flake8',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0',
            'twine>=5.0'
        ]
    },
    python_requires=">3.7",
    entry_points={
        'console_scripts':[
            "pulse_linter = pulse_linter:main"
        ],
        'flake8.extension': [
            'NC = pulse_linter.Extensions.flake8_function_snake_case_checker.checker:SnakeCaseChecker',
            # 'SC101 = pulse_linter.Extensions.use_of_eval.checker:SecurityChecker',
            # 'SC102 = Extensions.common_patterns.constants:InsecurePatterns',
            'SC103 = pulse_linter.Extensions.package_scanner.bad_import:BadImports',
            'SC104 = pulse_linter.Extensions.package_scanner.bad_importfrom:BadImportfrom',
            # 'SC105 = pulse_linter.Extensions.common_patterns.attributes:BadAttributes',
            'SM101 = pulse_linter.add_ons.eval:EvalChecker',
            'SM102 = pulse_linter.add_ons.exec:ExecChecker',
        ],
    },
)


# commands used 1) python setup.py bdist_wheel, sdist, pip install .