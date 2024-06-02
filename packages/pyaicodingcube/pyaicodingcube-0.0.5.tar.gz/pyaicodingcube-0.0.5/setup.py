from setuptools import setup, find_packages

setup(
    name='pyaicodingcube',
    version='0.0.5',
    packages=find_packages(),
    install_requires=[
        # 의존하는 라이브러리를 여기에 나열하세요.
        # 예: 'numpy>=1.18.0',
    ],
    python_requires='>=3.10',
    description='It is a library for exmarscube',
    author='smartcubelabs',
)