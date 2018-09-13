import sys, os

from setuptools import setup


PROJECT_ROOT, _ = os.path.split(__file__)
PROJECT_NAME = 'borgbackup_notifications_multi_target'
COPYRIGHT = u"Copyright (c) 2016 - 2017 Lars Hupfeldt Nielsen, Hupfeldt IT"
PROJECT_AUTHORS = u"Lars Hupfeldt Nielsen"
PROJECT_EMAILS = 'lhn@hupfeldtit.dk'
PROJECT_URL = "https://github.com/lhupfeldt/" + PROJECT_NAME
SHORT_DESCRIPTION = 'Wrapper around borgbackup to provide easy configuration of multiple target and desktop notifications.'
LONG_DESCRIPTION = open(os.path.join(PROJECT_ROOT, "README.md")).read()


if __name__ == "__main__":
    setup(
        name=PROJECT_NAME.lower(),
        # version_command=('git describe', 'pep440-git'),
        author=PROJECT_AUTHORS,
        author_email=PROJECT_EMAILS,
        packages=[PROJECT_NAME, PROJECT_NAME + '.client', PROJECT_NAME + '.client.notifications'],
        package_dir={
            PROJECT_NAME: '.',
            PROJECT_NAME + '.client': 'client',
            PROJECT_NAME + '.client.notifications': 'client/notifications',
        },
        zip_safe=False,
        include_package_data=True,
        install_requires=['psutil>=4.0.0', 'multiconf>=8.1', 'appdirs>=1.4'],
        # setup_requires='setuptools-version-command~=2.2',
        test_suite='test',
        tests_require=['pytest>=3.0.5'],
        url=PROJECT_URL,
        description=SHORT_DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        license='BSD',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Environment :: X11 Applications',
            'Environment :: MacOS X',
            'Environment :: Win32 (MS Windows)',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: BSD License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Topic :: System :: Archiving :: Backup',
        ],
        entry_points='''
            [console_scripts]
            bbmt={}.client.backup:main
        '''.format(PROJECT_NAME),
    )
