import json
from abc import ABC, abstractmethod
from pathlib import Path

import yaml
from jinja2 import Environment, PackageLoader

import app.reports.convert as convert
import app.reports.report_lib as rlib
from app.reports.report import Report

_basedir = "/tmp"


class Reporter(ABC):
    def __init__(self, spec: dict):
        self.spec = spec

    @abstractmethod
    def collector(
        self,
        args: dict[str, str | float | int | bool],
        org_uid: str,
        api_key: str,
        api_url: str,
    ) -> list:
        return []

    @abstractmethod
    def processor(
        self,
        data: list,
        args: dict[str, str | float | int | bool],
    ) -> dict:
        return {}

    def renderer(
        self,
        context: dict,
        format: str,
        rid: str,
    ) -> Path:
        return self.render(context, format, rid)

    def generate_reports(
        self, r: Report, api_key: str, api_url: str
    ) -> dict[rlib.FORMATS, Path]:

        rv = {}

        # Get the data
        data = self.collector(
            args=r.input.report_args,
            org_uid=r.input.org_uid,
            api_key=api_key,
            api_url=api_url,
        )

        # Process the data to a lowest common denominator context
        # dict that can be used to render the report in multiple formats
        context = self.processor(data, r.input.report_args)

        # Render the report in all supported formats
        for fmt in self.spec["supported_formats"]:
            rv[fmt] = self.renderer(context, fmt, r.id)  # type: ignore

        return rv

    def render(self, context: dict, format: str, rid: str) -> Path:

        if format == "json":
            with open(f"{_basedir}/{rid}.json", "w") as f:
                json.dump(context, f)
            return Path(f"{_basedir}/{rid}.json")

        if format == "yaml":
            with open(f"{_basedir}/{rid}.yaml", "w") as f:
                yaml.dump(context, f)
            return Path(f"{_basedir}/{rid}.yaml")

        if format == "md":
            with open(f"{_basedir}/{rid}.md", "w") as f:
                f.write(self.render_with_template(format, context))
            return Path(f"{_basedir}/{rid}.md")

        if format == "pdf":
            if not Path(f"{_basedir}/{rid}.md").exists():
                self.render(context, "md", rid)
            if not Path(f"{_basedir}/{rid}.md").exists():
                raise ValueError(
                    "Markdown file could not be generated for PDF"
                )
            convert.md_to_pdf(f"{_basedir}/{rid}.md", f"{_basedir}/{rid}.pdf")
            return Path(f"{_basedir}/{rid}.pdf")

        if format == "html":
            if not Path(f"{_basedir}/{rid}.md").exists():
                self.render(context, "md", rid)
            if not Path(f"{_basedir}/{rid}.md").exists():
                raise ValueError(
                    "Markdown file could not be generated for HTML"
                )
            convert.md_to_html(
                f"{_basedir}/{rid}.md", f"{_basedir}/{rid}.html"
            )
            return Path(f"{_basedir}/{rid}.html")

        raise ValueError(f"Unsupported format: {format}")

    def render_with_template(self, format, context):
        environment = Environment(
            loader=PackageLoader("app.reports.portfolio", "templates")
        )
        template_spec = self.spec["templates"][format]
        template = environment.get_template(template_spec)
        return template.render(context)
