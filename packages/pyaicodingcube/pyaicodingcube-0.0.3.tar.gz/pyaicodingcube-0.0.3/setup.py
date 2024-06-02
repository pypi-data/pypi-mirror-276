from setuptools import setup, find_packages

setup(
    name='pyaicodingcube',
    version='0.0.3',
    packages=['pyaicodingcube'],
    package_data={'pyaicodingcube': ['*.py']},
    include_package_data=True,
    python_requires='>=3.10',
    # 추가 메타데이터 및 의존성 정보 작성
)