from setuptools import setup

setup(
    name="chatmemoryc",
    version="0.1.4rc5",
    url="https://github.com/f6844710/chatmemoryc",
    author="pino",
    author_email="f6844710@nifty.com",
    maintainer="pino",
    maintainer_email="f6844710@nifty.com",
    description="Long-term and medium-term memories between you and chatbot",
    long_description=open("README.md",'r',encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    install_requires=["fastapi==0.110.0", "anthropic==0.28.0", "requests==2.31.0", "SQLAlchemy==2.0.28", "uvicorn==0.28.1", "pycryptodome==3.20.0"],
    license="Apache v2",
    packages=["chatmemoryc"],
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)
