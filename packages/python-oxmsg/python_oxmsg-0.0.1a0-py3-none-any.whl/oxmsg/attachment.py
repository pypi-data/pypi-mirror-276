"""The interface object for an attachment in an Outlook MSG file."""

from __future__ import annotations

import datetime as dt
from typing import Iterator

from oxmsg.domain import constants as c
from oxmsg.domain import model as m
from oxmsg.properties import Properties
from oxmsg.util import lazyproperty


class Attachment:
    """A file attached to an Outlook email message."""

    def __init__(self, storage: m.StorageT):
        self._storage = storage

    @lazyproperty
    def attached_by_value(self) -> bool:
        """The PidTagAttachDataBinary property contains the attachment data.

        This is as opposed to "by-reference" where only a path or URL is stored.
        """
        attach_method = self.properties.int_prop_value(c.PID_ATTACH_METHOD)
        assert attach_method is not None
        return bool(attach_method & m.AF_BY_VALUE)

    def dump_properties(self) -> str:
        """Report of message properies suitable for writing to the console."""

        def iter_lines() -> Iterator[str]:
            yield ""
            yield "---------------------"
            yield "Attachment Properties"
            yield "---------------------"
            yield ""
            yield "distinguished-properties"
            yield "------------------------"
            yield f"filename:          {self.filename}"
            yield f"MIME-type:         {self.mime_type}"
            yield f"size:              {self.size:,}"
            yield f"attached-by-value: {self.attached_by_value}"
            yield f"last-modified:     {self.last_modified}"
            yield ""
            yield "other properties"
            yield self.properties.dump()

        return "\n".join(iter_lines())

    @lazyproperty
    def file_bytes(self) -> bytes | None:
        """The attachment binary, suitable for saving to a file when detaching."""
        return self.properties.binary_prop_value(c.PID_ATTACH_DATA_BINARY)

    @lazyproperty
    def filename(self) -> str | None:
        """The full name of this file as it was originally attached.

        Like "FY24-quarterly-projections.xlsx". Does not include a path.
        """
        return self.properties.str_prop_value(c.PID_ATTACH_LONG_FILENAME)

    @lazyproperty
    def last_modified(self) -> dt.datetime | None:
        """Timezone-aware UTC datetime when this attachment was last modified.

        `None` if this property is not present on the attachment.
        """
        self.properties.date_prop_value(c.PID_LAST_MODIFICATION_TIME)

    @lazyproperty
    def mime_type(self) -> str | None:
        """ISO 8601 str representation of time this attachment was last modified."""
        return self.properties.str_prop_value(c.PID_ATTACH_MIME_TAG) or "application/octet-stream"

    @lazyproperty
    def properties(self) -> Properties:
        """Provides access to the properties of this OXMSG object."""
        return Properties(self._storage, properties_header_offset=m.ATTACH_HDR_OFFSET)

    @lazyproperty
    def size(self) -> int:
        """Length in bytes of this attachment."""
        return len(self.file_bytes) if self.file_bytes else 0
