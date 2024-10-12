## Documentation

Go to url: http://localhost:8002/docs

## Install local

- Create a virtual environment

```bash
python3 -m venv venv
```

- Activate the virtual environment in linux or mac

```bash
source venv/bin/activate
```

- Activate the virtual environment in windows

```bash
venv\Scripts\activate
```

- Install the dependencies

```bash
pip install -r requirements.txt
```

- Run the application

```bash
uvicorn main:app --reload
```