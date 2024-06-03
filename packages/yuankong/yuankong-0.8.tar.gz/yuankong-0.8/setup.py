from setuptools import setup, find_packages

setup(
    name='yuankong',
    version='0.8',
    packages=find_packages(),
    description='Basic function of YuankongAI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # 这使得README.md可以正确渲染
    author='ltq_yuankong',
    author_email='1539365976@qq.com',
    # url='http://60.205.141.203:3000/ningkp/MetaAgent/src/user_isolation',
    # install_requires=[
    #     # 依赖列表
    #     'numpy',
    #     'requests',
    # ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
