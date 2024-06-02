from setuptools import setup, find_packages

setup(
    name='rolyson',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Adicione aqui as dependências, se houver
    ],
    description='Biblioteca de funções comuns para meus projetos Django',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Rolyson',
    author_email='rolysonrocha@gmail.com',
    url='https://github.com/Rolyson/lib-rolyson',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
