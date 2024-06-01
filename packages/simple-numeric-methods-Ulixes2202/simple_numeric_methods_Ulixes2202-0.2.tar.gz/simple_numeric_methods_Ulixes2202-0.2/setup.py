from setuptools import setup, find_packages

# Diesesn Befehl in der Konsole ausführen, um das Package zu erstellen oder updaten
# python setup.py sdist bdist_wheel
setup(
    name='simple_numeric_methods_Ulixes2202',
    version='0.2',
    packages=find_packages(),
    install_requires=[],
)
# Um das Package zu erstellen, davor am besten noch die Version veränder
# python setup.py sdist bdist_wheel
# Um das Paket lokal zu testen
# pip install dist\simple_numeric_methods_Ulixes2202-0.1-py3-none-any.whl --force-reinstall 
# Um das Paket dann online zu stellen
# twine upload dist/*
# man wird dann nach dem API token gefragt, der ist in der Textdatei drin, einfach kopieren
# und mit einem rechtsklick einfügen. Es ist normal, dass man nichts sieht.