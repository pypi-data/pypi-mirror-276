import json
import os

import pytest

from app.reports.report import Report
from app.reports.report_engine import ReportEngine
from app.reports.report_lib import ReportInput

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")
ORG = os.getenv("ORG")
CI = os.getenv("CI") is not None

@pytest.fixture()
def engine():
    yield ReportEngine(
        {"backend": {"kind": "simple_file", "dir": "/tmp/reports"}}
    )


def report(filename: str):
    import os

    cwd = os.getcwd()
    fname = (
        filename
        if filename.startswith("/") or filename.startswith("./")
        else cwd + f"/app/reports/portfolio/testdata/{filename}"
    )
    with open(fname) as f:
        report_input = json.load(f)
        report_input["org_uid"] = ORG
        ri = ReportInput.model_validate(report_input)
        rep = Report(input=ri, formats=["json", "yaml", "md", "html", "pdf"])
        return rep


def test_report_agent_metrics(engine):
    if not API_KEY or not API_URL or not ORG:
        pytest.skip("Skipping test without API_KEY, API_URL, ORG")
    if CI:
        pytest.skip("Skipping test in CI")

    ri = report("repagent.json")
    reports = engine.make_reports(ri, API_KEY, API_URL)
    for fmt, path in reports.items():
        assert path.exists()
        if fmt != "pdf":
            assert path.read_text() != ""
            if fmt not in ["json", "yaml"]:
                assert "Spyderbat agent usage report" in path.read_text()


def test_report_ops(engine):
    if not API_KEY or not API_URL or not ORG:
        pytest.skip("Skipping test without API_KEY, API_URL, ORG")
    if CI:
        pytest.skip("Skipping test in CI")

    ri = report("repops.json")
    reports = engine.make_reports(ri, API_KEY, API_URL)
    for fmt, path in reports.items():
        assert path.exists()
        if fmt != "pdf":
            assert path.read_text() != ""
            if fmt not in ["json", "yaml"]:
                assert "Operational report" in path.read_text()


if __name__ == "__main__":
    import sys

    API_KEY = sys.argv[2]
    API_URL = sys.argv[3]
    rep = report(sys.argv[1])
    engine = ReportEngine(
        {"backend": {"kind": "simple_file", "dir": "/tmp/reports"}}
    )
    reports = engine.make_reports(rep, API_KEY, API_URL)
    print(reports)
