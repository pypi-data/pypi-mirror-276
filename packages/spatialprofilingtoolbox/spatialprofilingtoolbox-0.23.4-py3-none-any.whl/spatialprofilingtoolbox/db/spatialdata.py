"""Export to SpatialData format."""

from spatialdata import SpatialData
from spatialprofilingtoolbox.db.database_connection import DBCursor

class SpatialDataExporter:
    """Export to SpatialData format."""

    @classmethod
    def export(cls, database_config_file: str | None=None, study: str]) -> SpatialData:
        container = SpatialData()
        return container
