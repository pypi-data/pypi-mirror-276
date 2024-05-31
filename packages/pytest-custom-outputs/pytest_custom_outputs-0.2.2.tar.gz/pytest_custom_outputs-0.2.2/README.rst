
Enhance Your Pytest Reporting with Customizable Test Outputs

Tired of the standard pass/fail binary in pytest? With pytest-custom_outputs, you can create expressive and informative custom test results that go beyond the ordinary.  Tailor your reports to provide deeper insights into your test scenarios.

Useful for if you want more than just the default Pass, Fail, and Skip outcomes.


Features
--------

- Flexible Output Types: Define new outcome types like "unimplemented", "soft_fail"," "inconclusive," or any custom label that suits your testing needs.
- Fully Customizeable: Custom outputs are customizable in their name, description, result code, tag, and color.
- Seamless Integration: Easily incorporate custom outputs into your existing pytest test suites.
- Terminal and File Reporting: View your custom outputs in both your terminal output and pytest file reports.


Installation
------------

```bash
pip install pytest-custom_outputs
```


Usage
-----

In the directory where you will be running your pytest, create a file called "pytest_custom_outputs.json".
You will use this file to create your own custom outputs.
Feel free to copy and paste the below json file into yours and edit from there.

EXAMPLE FILE:
```python
{
        "custom_outputs": {
                "Pass_with_exception": {
                        "desc":"passed_with_exception",
                        "code":"P",
                        "tag":"XPASSED",
                        "color":"green"
                },
                "Fatal_failed": {
                        "desc":"fatal_failed",
                        "code":"!",
                        "tag":"FAILED",
                        "color":"red"
                },
                "Not_available": {
                        "desc":"not_available",
                        "code":"N",
                        "tag":"NOT_AVAILABLE",
                        "color":"blue"
                },
                "Failed_but_proceed": {
                        "desc":"failed_but_proceed",
                        "code":"X",
                        "tag":"FAILED_BUT_PROCEED",
                        "color":"red"
                },
                "Unimplemented": {
                        "desc":"unimplemented",
                        "code":"U",
                        "tag":"UNIMPLEMENTED",
                        "color":"yellow"
                },
                "Skipped": {
                        "desc":"skipped",
                        "code":"S",
                        "tag":"SKIPPED",
                        "color":"yellow"
                }
        }
}

```


custom_outputs
 - A dictionary with all the custom outputs inside of it. You can edit, delete, and add new outputs here.

Each custom output is denoted by a name. The name is also the key for that output
For example, in the above example file, "Pass_with_exception" and "Fatal_failed" are the names for their respective output.
Names are also how we determine the result of a test case. 
We use the c_assert function and enter the name as an argument to assert that specific output.

For example:
```python
import pytest
from pytest_custom_outputs import c_assert

def test_1():
    c_assert("Pass_with_exception")
```

In the example above, test_1 will result in "passed_with_exception".

If we put a name that is not in our custom output in the c_assert parameter, then it will assert the unknown outcome
Because of this, it is recommended to not make a custom output with the name "unknown"

The rest of the information in the json file can be edited and customized to your liking.


Why pytest-custom_outputs?
--------------------------

- Improved Communication: Get more informative insights from your test runs
- Focus on Key Areas: Prioritize test cases that require attention
- Tailored for Your Needs: Adapt outcomes and messages to your project's specific requirements


Contributing
------------

Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.


License
-------

Distributed under the terms of the `BSD-3`_ license, "pytest-custom_outputs" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`file an issue`: https://github.com/MichaelE55/pytest-custom_outputs/issues
