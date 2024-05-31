import pytest
import json
from pytest import skip

_pcode = "PYTESTCUSTOMOUTPUTSCODE5567PCU_"
_attrcode = "_PCOCODE5568PCU_"

def c_assert(code):
    skip(_pcode+code)

def pytest_addoption(parser):
    group = parser.getgroup('custom_outputs')
    group.addoption(
        '--custom_output',
        action='store',
        dest='custom_output_loc',
        default='pytest_custom_outputs.json',
        help='Select the custom output file to use.'
    )


def pytest_sessionstart(session):
    session.config.custom_output_valid = True
    col = session.config.getoption('custom_output_loc')
    try:
        f = open(col)
        data = json.load(f)
    except:
        session.config.custom_output_valid = False
    if session.config.custom_output_valid:
        #session.config.custom_output_unknown = data["unknown"]
        session.config.custom_output = data["custom_outputs"]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    report = (yield).get_result()
    if report.skipped and call.excinfo.typename != "AssertionError":
        if _pcode in str(call.excinfo):
            if item.config.custom_output_valid:
                data = item.config.custom_output
                splitstr = str(call.excinfo).split(_pcode)[1]
                cname = splitstr.split(" tblen")[0]
                isFound = False
                for name in data:
                    if name == cname:
                        setattr(report, _attrcode+name, True)
                        isFound = True
                if not isFound:
                    setattr(report, _attrcode+"unknown", True)
            else:
                setattr(report, _attrcode+"unknown", True)


def pytest_report_teststatus(report, config):
    if config.custom_output_valid:
        data = config.custom_output
        for name in data:
            if getattr(report, _attrcode+name, False):
                return data[name]["desc"],data[name]["code"],(data[name]["tag"], {data[name]["color"]: True})
    if getattr(report, _attrcode+"unknown", False):
        return "unknown","?",("UNKNOWN", {"purple": True})
