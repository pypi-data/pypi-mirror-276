from pathlib import Path

from glabpkg.version import __version__
from pkglts.dependency import Dependency
from pkglts.option.doc.badge import Badge
from pkglts.option_object import Option


class OptionGlabReport(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def update_parameters(self, cfg):
        cfg['doc']['fmt'] = "rst"

        cfg['sphinx']['doc_dir'] = "report"
        cfg['sphinx']['theme'] = "sphinx_rtd_theme"

        # add a parameter to the option
        return super().update_parameters(cfg)

    def check(self, cfg):
        invalid_params = []

        return invalid_params

    def require_option(self, cfg):
        return ['glabbase', 'sphinx']

    def require(self, cfg):
        yield Dependency("sphinxcontrib-svg2pdfconverter", intent="report", pkg_mng="pip")

    def environment_extensions(self, cfg):
        if "/" in cfg['gitlab']['owner']:
            gr = cfg['gitlab']['owner'].split("/")
            group_owner = gr[0]
            subgroup_owner = "/".join(gr[1:]) + "/"
        else:
            group_owner = cfg['gitlab']['owner']
            subgroup_owner = ""

        url = f"https://{group_owner}.gitlab.io/{subgroup_owner}{cfg['gitlab']['project']}/"
        img = f"{url}_images/badge_doc.svg"
        badge = Badge(
            name="doc",
            url=url,
            url_img=img,
            text="Documentation status"
        )

        return {"badges": [badge]}
