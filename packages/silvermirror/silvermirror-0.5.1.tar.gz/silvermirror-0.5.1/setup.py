from setuptools import setup

version = '0.5.1'
description = "mirror files across hosts"

setup(name='silvermirror',
      version=version,
      description=description,
      long_description=description,
      classifiers=[],
      keywords='mirror unison',
      author='Jeff Hammel',
      author_email='k0scist@gmail.com',
      url='http://k0s.org/hg/silvermirror',
      license='GPL',
      packages=['silvermirror'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'martINI >= 0.6',
          'netifaces',
          'pexpect',
          'python-hglib',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      silvermirror = silvermirror.unify:main
      mirror-hg = silvermirror.hg:main

      [silvermirror.reflectors]
      unison = silvermirror.unison:unison
      """,
      )
