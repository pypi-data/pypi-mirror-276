from setuptools import setup


# List of requirements
requirements = [
    'pyyaml', # no-bump
'luminesce-sdk-preview==1.14.758', # no-bump
'lusid-jam==0.1.2', # no-bump
'lusid-sdk-preview==1.1.120', # no-bump
'fbnlab-preview==0.1.108', # no-bump
'finbourne-access-sdk==0.0.3751', # no-bump
'finbourne-identity-sdk==0.0.2834', # no-bump
'finbourne-insights-sdk-preview==0.0.763', # no-bump
'finbourne-sdk-utilities==0.0.10', # no-bump
'lusid-configuration-sdk-preview==0.1.514', # no-bump
'lusid-drive-sdk-preview==0.1.617', # no-bump
'lusid-notifications-sdk-preview==0.1.923', # no-bump
'lusid-scheduler-sdk-preview==0.0.829', # no-bump
'lusid-workflow-sdk-preview==0.1.810', # no-bump
'lusidtools==1.0.14', # no-bump
'dve-lumipy-preview==0.1.1075', # no-bump

]




setup(
    name='lusid_bundle',
    version='0.0.7',
    install_requires=requirements,
    description='lusid-bundle is a python package that makes it quick and easy to install all of the Lusid and Luminesce sdks and dependencies.',
    long_description=open('README.md').read(),
    include_package_data=True,  
    long_description_content_type='text/markdown',
    author='Orlando Calvo',
    author_email='orlando.calvo@finbourne.com',
    url='https://gitlab.com/orlando.calvo1/lusid-bundle',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)