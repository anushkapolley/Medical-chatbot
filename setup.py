from setuptools import find_packages, setup

setup(
    name="medical_chatbot",
    version="0.1.0",
    author="Anushka polley",
    author_email="anushkapolley23@gmail.com",
    packages=find_packages(),
    #find_packages() will try to find thr constructor file "__init__.py" 
    #where ever constructor file is there it will store as local packages
    install_requires=[]
    #this will all the requirements from .txt and install them
)