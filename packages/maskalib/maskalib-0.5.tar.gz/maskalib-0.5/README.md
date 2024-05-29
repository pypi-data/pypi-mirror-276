# Maskalib

Maskalib is a Python library for [describe the purpose of your library].

## Installation

You can install Maskalib using pip:

```bash
pip install maskalib
```

## How to use the free version ?

```bash
from maskalib import MaskaAI

MODEL = "MaskaAI" # MODEL NAME: MaskaAI (BEST), FibiAI, ScenarioAI, GoogleAI, MicroAI
MESSAGETOASK = "" # ASK ANYTHING
APIKEY = "" # Your Maska.ai API KEY
x = MaskaAI(MODEL, MESSAGETOASK, APIKEY)
print(x[0]) #Status
print(x[1]) #Title
print(x[2]) #Response

```

## How to use the Premium version ?

```bash
from maskalib import MaskaAI

MODEL = "MaskaAI" # MODEL NAME: MaskaAI (BEST), FibiAI, ScenarioAI, GoogleAI, MicroAI
YourAINAME = "" # what you want the AI to be called
MESSAGETOASK = "" # ASK ANYTHING
APIKEY = "" # Your Maska.ai API KEY (Make sure to buy Premium)
x = MaskaAI(MODEL, YourAINAME,  MESSAGETOASK, APIKEY)
print(x[0]) #Status
print(x[1]) #Title
print(x[2]) #Response

```

# Go to Maska.ai to know more :D