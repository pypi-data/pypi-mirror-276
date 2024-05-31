from setuptools import setup, find_packages

setup(
    name="LangRAGEval",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "sacrebleu",
        "rouge-score",
        "bert-score",
        "langchain",
        "pydantic",
    ],
    entry_points={
        'console_scripts': [
            'langrageval=langrageval:main',
        ],
    },
    author="Prashant Verma",
    author_email="prashant27050@gmail.com",
    description="LangRAGEval is a library for evaluating responses based on faithfulness, context recall, answer relevancy, and context relevancy.",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Vprashant/LangGPTEval",
)

