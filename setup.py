from setuptools import setup, find_packages
from typing import List


requirement_list = []

def get_requirements() -> List[str]:
    """ 
    This function will return list of requirements
    """
    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()
            
            for line in lines:
                requirement = line.strip()
                
                if requirement != '-e .':
                    requirement_list.append(requirement)
                    
        return requirement_list
    
    except Exception as e:
        raise FileNotFoundError("requirements.txt file not found")
    
     
setup(
    name='networksecurity',
    version='0.0.1',
    author='Sowmya AM',
    author_email='sowmya.anekonda@gmil.com',
    packages=find_packages(),
    install_requires=get_requirements()
)