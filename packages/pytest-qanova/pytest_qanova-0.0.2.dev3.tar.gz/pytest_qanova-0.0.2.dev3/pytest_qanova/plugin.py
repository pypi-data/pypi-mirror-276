import pytest
import json
import os

test_info_dict = {}
session_info = {}


def pytest_configure(config):
    """Hook to configure pytest and collect starting variables."""
    session_info['command_line'] = ' '.join(config.invocation_params.args)
    session_info['rootdir'] = str(config.rootdir)
    session_info['inifile'] = str(config.inifile) if config.inifile else None
    session_info['args'] = config.args
    session_info['options'] = {key: value for key, value in vars(config.option).items()}


def pytest_collection_modifyitems(config, items):
    for item in items:
        nodeid = item.nodeid
        test_info_dict[nodeid] = {
            'nodeid': nodeid,
            'name': item.name,
            'path': str(item.fspath),
            'location': item.location,
            'markers': [{marker.name: marker.kwargs if marker.kwargs else None} for marker in item.iter_markers()],
            'setup': {'outcome': None, 'duration': None},
            'call': {'outcome': None, 'duration': None},
            'teardown': {'outcome': None, 'duration': None},
            }


def pytest_runtest_logreport(report):
    nodeid = report.nodeid
    if nodeid in test_info_dict:
        phase = report.when
        test_info_dict[nodeid][phase]['outcome'] = report.outcome
        test_info_dict[nodeid][phase]['duration'] = report.duration
        if report.outcome == 'failed':
            error_type, error_message = extract_error_type(report)
            test_info_dict[nodeid][phase]['longrepr'] = str(report.longrepr) if report.failed else None
            test_info_dict[nodeid][phase]['error_type'] = error_type
            test_info_dict[nodeid][phase]['error_message'] = error_message


def extract_error_type(report):
    if report.failed:
        if hasattr(report.longrepr, 'reprcrash'):
            error_type, error_message = report.longrepr.reprcrash.message.split(': ')
            return error_type, error_message
    else:
        return None, None


def pytest_sessionfinish(session, exitstatus):
    pytest_worker = os.environ.get("PYTEST_XDIST_WORKER")
    if pytest_worker == 'gw0':
        with open('test_results.json', 'w') as f:
            json.dump({
                'session_info': session_info,
                'tests': list(test_info_dict.values())
                }, f, indent=4)

