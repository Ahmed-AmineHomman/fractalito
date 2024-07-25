# Fractalito

Fractalito is a lightweight web app allowing you to compute beautiful fractals from various mathematical equations.
It is made with :heart: with [Gradio](https://gradio.app/).

:warning: **Warning** :warning::  
Fractalito is a project I made for fun, and is far from being the best fractal-producing software.
I strongly recommend to use other pieces of software if you're looking for efficiency when computing fractals.
You will find [here](https://fractalfoundation.org/resources/fractal-software/) a list of fractal computing pieces of software compiled by the [Fractal Foundation](https://fractalfoundation.org/).

## Getting started

Clone this deposit on your system and install the dependencies by opening your favorite terminal in the folder where you cloned this deposit and typing the following command:
```shell
python -m pip install -r requirements.txt
```

**Remark**: if you do not wish to alter your main python interpreter, we recommend to use a virtual environment when installing Fractalito's dependencies.

You can then run the solution by executing the [`app.py`](app.py) script with your interpreter:
```shell
python app.py
```

The gradio server will then start and indicate you a URL at which you can access the app.

The gradio server accepts various parameters for sharing or debugging purposes. You can access the parameters' help with the following command:

```shell
python app.py --help
```
