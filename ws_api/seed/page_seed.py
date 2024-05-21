from ..repositories import page
from ..schemas.page import PageSchema

Pages = [
    {"name": "Analysis", "icon": "IoCameraOutline", "route": "analysis"},
    {"name": "Results", "icon": "IoStatsChartOutline", "route": "result"},
    {"name": "Mode", "icon": "IoEyedropOutline", "route": "mode"},
    {"name": "Settings", "icon": "IoOptionsOutline", "route": "settings"},
]


def seed_page():
    for pg in Pages:
        page_dump = PageSchema().dump(pg)
        name, icon, route = page_dump.values()
        page.insert(name, icon, route)
