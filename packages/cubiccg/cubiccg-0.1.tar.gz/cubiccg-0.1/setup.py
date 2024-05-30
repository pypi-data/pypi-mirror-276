from setuptools import setup, find_packages

setup(
    name='cubiccg',
    version='0.1',
    packages=find_packages(),
    install_requires=["torch>=2.2.2"],
    entry_points={
        'console_scripts': [
            'my_package_script = my_package.module1:main_function',
        ],
    },
    author='kevin',
    author_email='kevin2059@163.com',
    description='cubic cg for learning',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url='https://github.com/your_username/my_package',
    license='MIT',
)
