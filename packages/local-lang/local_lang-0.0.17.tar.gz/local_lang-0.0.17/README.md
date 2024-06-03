# LocalLang

**Installation**

```commandline
pip install local-lang
```

**Description**

LocalLang is a simple library to manage localization in your python program.
It allows you to create a json file for each language you want to support.
You can use placeholders in your translation and specify the type of the placeholder.
You can also specify the format for the `datetime` and `time` type.

This package converts your json file to a Python class with all your translation.
You can then use this class to get your translation.

**Usage**

```bash
locallang --help  # Show help
locallang --default-lang en  # Reload localisation
locallang  # Reload localisation but the default language is en_us
locallang --version  # Show version
```

**Json file structure**

*`placeholders` is optional*

*`no_f_string` is optional*
- This parameter is used to disable the use of f-string in the localization if you use {} in your translation.

*`format` is only for `datetime` and `time` type*

```json
{
  "key": "value {placeholder_name}",
  "@key": {
    "no_f_string": "bool",
    "placeholders": {
      "placeholder_name": {
        "type": "str|int|float|bool|datetime|time",
        "format": "format"
      }
    }
  }
}
```

**Example**


`test.py`

```python
from locallang import LangInit, getLocalisation
import datetime

localisation = LangInit()

local = getLocalisation(local="en_us")

print(local.hey())
print(local.hello_world())
print(local.toDay(date=datetime.datetime.now()))
print(local.thisTime(time=datetime.datetime.now().time()))
print(local.testStr(strText="Hello world!"))
print(local.testInt(intNum=1))
print(local.testFloat(floatNum=1.5))
print(local.testBool(boolValue=True))
print(local.test(test=1.5))

local = getLocalisation(local="fr")

print(local.hey())
print(local.hello_world())
print(local.toDay(date=datetime.datetime.now()))
print(local.thisTime(time=datetime.datetime.now().time()))
print(local.testStr(strText="Bonjour tout le monde !"))
print(local.testInt(intNum=2))
print(local.testFloat(floatNum=2.5))
print(local.testBool(boolValue=False))
print(local.test(test="coucou"))
```

`en_us.json`
```json
{
    "hey": "Hey!",
    "hello_world": "Hello world!",
    "toDay": "Date: {date}",
    "@toDay": {
        "placeholders": {
            "date": {
                "type": "datetime",
                "format": "%Y/%m/%d %H:%M"
            }
        }
    },
    "thisTime": "Time: {time}",
    "@thisTime": {
        "placeholders": {
            "time": {
                "type": "time",
                "format": "%H:%M"
            }
        }
    },
    "testStr": "Test: {strText}",
    "@testStr": {
        "placeholders": {
            "strText": {
                "type": "str"
            }
        }
    },
    "testInt": "Test: {intNum}",
    "@testInt": {
        "placeholders": {
            "intNum": {
                "type": "int"
            }
        }
    },
    "testFloat": "Test: {floatNum}",
    "@testFloat": {
        "placeholders": {
            "floatNum": {
                "type": "float"
            }
        }
    },
    "testBool": "Test: {boolValue}",
    "@testBool": {
        "placeholders": {
            "boolValue": {
                "type": "bool"
            }
        }
    },
    "test": "Test: {test}"
}
```

`fr.json`
```json
{
    "hey": "Coucou !",
    "hello_world": "Bonjour tout le monde!",
    "toDay": "Date: {date}",
    "thisTime": "Time: {time}",
    "testStr": "Test: {strText}",
    "testInt": "Test: {intNum}",
    "testFloat": "Test: {floatNum}",
    "testBool": "Test: {boolValue}",
    "test": "Test: {test}"
}
```

`result in consol`
```text
Hey!
Hello world!
Date: 2023/05/07 00:15
Time: 00:15
Test: Hello world!
Test: 1
Test: 1.5
Test: True
Test: 1.5
Coucou !
Bonjour tout le monde!
Date: 2023/05/07 00:15
Time: 00:15
Test: Bonjour tout le monde !
Test: 2
Test: 2.5
Test: False
Test: coucou
```
