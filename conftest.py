import pytest

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    # add Description on report.html
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
