from setuptools import setup

setup(name='cellworld_tlppo',
      author='German Espinosa',
      author_email='germanespinosa@gmail.com',
      long_description=open('./cellworld_tlppo/README.md').read() + '\n---\n<small>Package created with Easy-pack</small>\n',
      long_description_content_type='text/markdown',
      packages=['cellworld_tlppo'],
      install_requires=['cellworld_game', 'cellworld_gym', 'scikit-learn'],
      license='MIT',
      include_package_data=True,
      version='0.0.15',
      zip_safe=False)
