# Casino Simulator

This is a simple casino simulator using Python and MySQL.

## Requirements

The program won't work for you as the server is local.
You can make your own local MySQL server to try the application.
First you will need the following packages:

- [Python +3.6](https://www.python.org/downloads/)
- [MySQL](https://dev.mysql.com/downloads/connector/python/)
- [MySQL Connector](https://pypi.org/project/mysql-connector-python)
- [cryptocode](https://pypi.python.org/pypi/cryptocode)

These packages can easily be installed using the following commands:

```sh
pip install -r requirements.txt
```

MySQL has to be installed separately.

---

## Usage

After installing the packages, you have to setup the database and key for cryptocode.
You can use `setup_sql.py` to do this.

```sh
python setup_sql.py
```

Then you can run the main program.

```sh
python main.py
```
