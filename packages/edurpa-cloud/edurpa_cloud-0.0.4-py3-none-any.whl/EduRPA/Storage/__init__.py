name = 'edurpa_storage'
from .S3Storage import S3Storage
from robotlibcore import DynamicCore

class Storage(DynamicCore):
    def __init__(
        self
    ):
        # Register keyword libraries to LibCore
        libraries = [
            S3Storage()
        ]
        super().__init__(libraries)