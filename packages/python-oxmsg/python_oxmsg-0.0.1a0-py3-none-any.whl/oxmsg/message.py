"""The main interface object for an Outlook MSG file."""

from __future__ import annotations

import datetime as dt
import email.message
import email.parser
import json
import os
import struct
from typing import IO, Iterator

from olefile import OleFileIO, isOleFile

from oxmsg.attachment import Attachment
from oxmsg.domain import constants as c
from oxmsg.domain import model as m
from oxmsg.domain.encodings import encoding_from_codepage
from oxmsg.properties import Properties
from oxmsg.recipient import Recipient
from oxmsg.storage import Storage
from oxmsg.util import lazyproperty


class Message:
    """An Outlook email message loaded from an OXMSG format (.msg) file."""

    def __init__(self, storage: m.StorageT):
        self._storage = storage

    @classmethod
    def load(cls, msg_file: str | IO[bytes] | bytes) -> Message:
        """Load an instance from `msg_file`.

        `msg_file` can be a file-path, a file-like object, or the bytes of the MSG file.
        """
        # -- ensure magic bytes on file are as expected --
        is_olefile = (
            isOleFile(data=msg_file) if isinstance(msg_file, bytes) else isOleFile(msg_file)
        )
        if not is_olefile:
            filename = os.path.basename(msg_file) if isinstance(msg_file, str) else "msg_file"
            raise ValueError(f"{filename} is not an Outlook MSG file")

        with OleFileIO(msg_file) as ole:
            root_storage = Storage.from_ole(ole)

        self = cls(root_storage)
        self._validate()
        return self

    @lazyproperty
    def attachment_count(self) -> int:
        """Number of attachments on this message."""
        return self._header_prop_values[3]

    @lazyproperty
    def attachments(self) -> tuple[Attachment, ...]:
        """Attachment object for each attachment in this message."""
        return tuple(self._iter_attachments())

    @lazyproperty
    def body(self) -> str | None:
        """True if this message includes a non-empty HTML body property."""
        return self.properties.str_prop_value(c.PID_BODY)

    def dump_properties(self) -> str:
        """A summary of this MS-OXMSG object's top-level properties."""
        string_props_are_unicode = (
            self.properties._string_props_are_unicode  # pyright: ignore[reportPrivateUsage]
        )
        str_prop_encoding = (
            self.properties._str_prop_encoding  # pyright: ignore[reportPrivateUsage]
        )

        internet_code_page = self.properties.int_prop_value(0x3FDE)
        internet_encoding = (
            None if internet_code_page is None else encoding_from_codepage(internet_code_page)
        )

        def iter_lines() -> Iterator[str]:
            yield "header-properties"
            yield "-----------------"
            yield f"next_recipient_id: {self._header_prop_values[0]}"
            yield f"next_attachment_id: {self._header_prop_values[1]}"
            yield f"recipient_count: {self._header_prop_values[2]}"
            yield f"attachment_count: {self._header_prop_values[3]}"
            yield ""
            yield "distinguished-properties"
            yield "------------------------"
            yield f"string_props_are_unicode: {string_props_are_unicode}"
            if not string_props_are_unicode:
                yield f"string_props_encoding:    {str_prop_encoding}"
            yield f"internet_code_page:       {internet_encoding}"
            yield f"subject:                  {repr(self.subject)}"
            yield f"message_headers: {json.dumps(self.message_headers, indent=4, sort_keys=True)}"
            yield ""
            yield "other properties"
            yield self.properties.dump()

        return "\n".join(iter_lines())

    @lazyproperty
    def html_body(self) -> str | None:
        """The HTML body of this message if it has it, `None` otherwise."""
        html_bytes = self.properties.binary_prop_value(c.PID_HTML)
        if html_bytes is None:
            return None
        return html_bytes.decode(self.properties.body_encoding)

    @lazyproperty
    def message_headers(self) -> dict[str, str]:
        """From, To, Content-Type, etc. headers for this message as {name: value} mapping."""
        return dict(self._message_headers)

    @lazyproperty
    def message_class(self) -> str:
        """Outlook Message Class identifier like "IPM.Note" for this message."""
        return self.properties.str_prop_value(c.PID_MESSAGE_CLASS) or "Unknown"

    @lazyproperty
    def properties(self) -> Properties:
        """Provides access to the properties of this OXMSG object."""
        return Properties(self._storage, properties_header_offset=m.MSG_HDR_OFFSET)

    @lazyproperty
    def recipients(self) -> tuple[Recipient, ...]:
        """`Recipient` object for each recipient of this message."""
        return tuple(self._iter_recipients())

    @lazyproperty
    def sender(self) -> str | None:
        """Name and email address of the message sender.

        Like '"Steve Canny" <stcanny@oxmsg.io>'.

        None if it is not recorded in the message. This may occur when the message is a draft or
        system-generated or perhaps in other cases.

        Note that the value of the From: message header is returned when present (usually I expect)
        and may contain multiple addresses separated by commas.
        """
        # -- start by looking in the message "From:" header --
        if from_header_value := self._message_headers["from"]:
            return from_header_value
        # -- assemble from parts --
        props = self.properties
        raw_name = (props.str_prop_value(c.PID_SENDER_NAME) or "").strip()
        name = f'"{raw_name}" ' if raw_name else ""
        email = props.str_prop_value(c.PID_SENDER_EMAIL_ADDRESS) or props.str_prop_value(
            c.PID_SENDER_SMTP_ADDRESS
        )
        return f"{name}<{email}>" if email else props.str_prop_value(c.PID_SENT_REPRESENTING_NAME)

    @lazyproperty
    def sent_date(self) -> dt.datetime | None:
        """When this message was submitted by the sender.

        This value will be `None` if the message has not been sent and possibly in other cases.
        """
        return self.properties.date_prop_value(c.PID_CLIENT_SUBMIT_TIME)

    @lazyproperty
    def subject(self) -> str:
        """Subject line of this message."""
        return self.properties.str_prop_value(c.PID_SUBJECT) or ""

    @lazyproperty
    def _header_prop_values(self) -> tuple[int, int, int, int]:
        """The property values in the MSG-root properties header.

        It is a tuple of the four int values:
         - next_recipient_id
         - next_attachment_id
         - recipient_count
         - attachment_count
        """
        return struct.unpack("<8x4I", self._storage.properties_stream_bytes[:24])

    def _iter_attachments(self) -> Iterator[Attachment]:
        """Generate `Attachment` object for each attachment in this message.

        Should need to be called at most once.
        """
        return (Attachment(storage) for storage in self._storage.iter_attachment_storages())

    def _iter_recipients(self) -> Iterator[Recipient]:
        """Generate `Recipient` object for each recipient in this message.

        Should need to be called at most once.
        """
        return (Recipient(storage) for storage in self._storage.iter_recipient_storages())

    @lazyproperty
    def _message_headers(self) -> email.message.Message:
        """From, To, Content-Type, etc. headers for this message as Message object.

        This provides case-insensitive access along with some other convenient behaviors not
        available from a `dict`.
        """
        headers = self.properties.str_prop_value(c.PID_TRANSPORT_MESSAGE_HEADERS) or ""
        return email.parser.HeaderParser().parsestr(headers)

    def _validate(self) -> None:
        """Raise if this message is invalid for one of a variety of possible reasons."""
        # -- for now, we only process email messages --
        # if not self.message_class.startswith("IPM.Note"):
        #     raise ValueError(f"{self.message_class} files not supported")
