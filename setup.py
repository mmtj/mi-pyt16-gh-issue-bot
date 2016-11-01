from setuptools import setup

with open('README.md') as f:
    long_description = ''.join(f.readlines())

setup(
    name='matejekm_gh_issue_bot',
    version='0.3.2',
    description='Robot for labeling issues in Github repository. Provided as two tools - cli and webapp.',
    long_description=long_description,
    author='Martin Matejek',
    author_email='martin.matejek@gmx.com',
    keywords=['github', 'issues', 'robot', 'flask'],
    license='MIT',
    url='https://github.com/matejekm/gh-issue-bot',
    packages=['matejekm_gh_issue_bot'],
    package_dir={'matejekm_gh_issue_bot': 'matejekm_gh_issue_bot'},
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Bug Tracking',
        'Natural Language :: English',
        'Framework :: Flask',
        'Environment :: Console'
    ],
    entry_points={
        'console_scripts': [
            'matejekm_gh_issue_bot = matejekm_gh_issue_bot.launcher:cli',
        ],
    },
    install_requires=['Flask', 'click', 'requests', 'markdown', 'configparser'],
    zip_safe=False
)
