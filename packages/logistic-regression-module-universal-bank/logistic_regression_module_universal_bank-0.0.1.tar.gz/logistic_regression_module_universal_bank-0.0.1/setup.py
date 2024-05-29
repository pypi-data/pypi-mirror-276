import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="logistic_regression_module_universal_bank", # 모듈 이름
    version="0.0.1", # 버전
    author="TaeMin", # 제작자
    author_email="taeminida@gmail.com", # contact
    description="로지스틱회귀 예제 1", # 모듈 설명
    long_description=open('README.md').read(), # README.md에 보통 모듈 설명을 해놓는다.
    long_description_content_type="text/markdown",
    install_requires=[ # 필수 라이브러리들을 포함하는 부분인 것 같음, 다른 방식으로 넣어줄 수 있는지는 알 수 없음
    "matplotlib==3.9.0", 
    "numpy==1.25.2", 
    "pandas==1.5.3", 
    "scikit_learn==1.4.2", 
    "statsmodels==0.14.2", 
    "mord==0.7", 
    "seaborn==0.13.2", 
    "dmba==0.2.4", 
    ],
    package_data={'': ['LICENSE.txt', 'requirements.txt']}, # 원하는 파일 포함, 제대로 작동되지 않았음
    include_package_data=True,
    packages = setuptools.find_packages(), # 모듈을 자동으로 찾아줌
    python_requires=">=3.9.13", # 파이썬 최소 요구 버전
)