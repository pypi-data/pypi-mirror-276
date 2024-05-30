import pytest
import json

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
        try:
            session.config.custom_output_use_unknown = data["use_unknown_if_no_match"]
            session.config.custom_output_unknown = data["unknown"]
        except:
            session.config.custom_output_use_unknown = False
        session.config.custom_output = data["custom_outputs"]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    report = (yield).get_result()
    if item.config.custom_output_valid:
        data = item.config.custom_output
        use_unknown = item.config.custom_output_use_unknown
        if report.skipped and call.excinfo.typename != "AssertionError":
            isFound = False
            for name in data:
                if name in str(call.excinfo):
                    setattr(report, data[name]["attribute"], True)
                    isFound = True
            if not isFound and use_unknown:
                data_unknown = item.config.custom_output_unknown
                setattr(report, data_unknown["attribute"], True)


def pytest_report_teststatus(report, config):
    if config.custom_output_valid:
        data = config.custom_output
        use_unknown = config.custom_output_use_unknown
        for name in data:
            if getattr(report, data[name]["attribute"], False):
                return data[name]["status"]["desc"],data[name]["status"]["code"],(data[name]["status"]["output"]["tag"], {data[name]["status"]["output"]["color"]: True})
        if use_unknown:
            data_unknown = config.custom_output_unknown
            if getattr(report, data_unknown["attribute"], False):
                return data_unknown["status"]["desc"],data_unknown["status"]["code"],(data_unknown["status"]["output"]["tag"], {data_unknown["status"]["output"]["color"]: True})

