from setuptools import setup

setup(name='osa',
      version='1.0',
      author='Arya Stevinson',
      author_email='arya.stevinson@gmail.com',
      packages=['osa',
                'osa.gui',
                'osa.exceptions',
                'osa.services',
                'osa.utils'],
      entry_points={
          'console_scripts': ['start_osa_gui=osa.gui.app:run'],
      })
