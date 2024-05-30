
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
        "use_unknown_if_no_match": true,
        "unknown": {
                "attribute":"_unknown",
                "status": {
                        "desc":"unknown",
                        "code":"?",
                        "output": {
                                "tag":"UNKNOWN",
                                "color":"purple"
                        }
                }
        },
        "custom_outputs": {
                "Pass_with_exception": {
                        "attribute":"_expected_pass",
                        "status": {
                                "desc":"passed_with_exception",
                                "code":"P",
                                "output": {
                                        "tag":"XPASSED",
                                        "color":"green"
                                }
                        }
                },
                "Fatal_failed": {
                        "attribute":"_fatal_fail",
                        "status": {
                                "desc":"fatal_failed",
                                "code":"!",
                                "output": {
                                        "tag":"FAILED",
                                        "color":"red"
                                }
                        }
                },
                "Not_available": {
                        "attribute":"_not_available",
                        "status": {
                                "desc":"not_available",
                                "code":"N",
                                "output": {
                                        "tag":"NOT_AVAILABLE",
                                        "color":"blue"
                                }
                        }
                },
                "Failed_but_proceed": {
                        "attribute":"_fail_but_proceed",
                        "status": {
                                "desc":"failed_but_proceed",
                                "code":"X",
                                "output": {
                                        "tag":"FAILED_BUT_PROCEED",
                                        "color":"red"
                                }
                        }
                },
                "Unimplemented": {
                        "attribute":"_unimplemented",
                        "status": {
                                "desc":"unimplemented",
                                "code":"U",
                                "output": {
                                        "tag":"UNIMPLEMENTED",
                                        "color":"yellow"
                                }
                        }
                },
                "Skipped": {
                        "attribute":"_skipped",
                        "status": {
                                "desc":"skipped",
                                "code":"S",
                                "output": {
                                        "tag":"SKIPPED",
                                        "color":"yellow"
                                }
                        }
                }
        }
}
```


use_unknown_if_no_match
 - If True, use the unknown output below if there is no match. Otherwise, use standard skip

unknown
 - The output to use if a test's result is not in default or custom outputs 

custom_outputs
 - A dictionary with all the custom outputs you write inside of it. You can edit, delete, and add new outputs here.


Each custom output is denoted by a name. The name is also the key for that output
For example, in the above example file, "Pass_with_exception" and "Fatal_failed" are the names for their respective output.
Names are also how we determine the result of a test case. 
This is done by using skip followed by the name in the parameter.

For example:
```python
import pytest
from pytest import skip

def test_1():
    skip("Pass_with_exception")
```

In the example above, test_1 will result in "passed_with_exception".
Because the name overrides the outcome, it will not result in a skip.
We use the keyword skip as a means to obtaining our desired outcome.

If we put a name that is not in our custom output in the skip parameter,
then the following occurs:
 - if we set unknown to True in the json, we will use the unknown outcome
 - else we will use the default skip and pass the name as a message (Standard skip behavior)


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
