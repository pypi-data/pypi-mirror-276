# astro-chronos

Ein Python Lernprojekt

## HOWTO

### Einstellung einer virtuellen Umgebung

Die virtuelle Umgebung wird im Ordner `.venv` angelegt.

```shell
python -m venv .venv 
```

Aktivierung der virtuellen Umgebung via

```shell
source .venv/bin/activate       # Aktivierung
python --version                # Überprüfung ob die VE aktiviert ist
pip install -e .                # Installiert das Projekt in der virtuelle Umgebung
```

### Run alle Testfälle

```shell
python -m unittest discover -p "*_test.py"
```


### Distribution (optional)

```shell
python3 -m pip install --upgrade build     # einmalig
python3 -m build
```

