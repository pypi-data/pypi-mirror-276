"""
Copyright 2020 GRENMap Authors

SPDX-License-Identifier: Apache License 2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

--------------------------------------------------------------------

Synopsis: GRENML parser. This file provides the ability to parse files
and streams into a provided GRENML manager
"""
import importlib_resources
import lxml.etree
import xml  # nosemgrep : use-defused-xml

from io import BytesIO, TextIOWrapper

from grenml import GRENMLManager
from grenml.parsing import GRENMLHandler


def load_schema():
    """
    Creates an lxml schema object, capable of validating XML input
    according to the GRENML schema.
    """
    schemas_traversable = importlib_resources.files('grenml.schemas')
    schema_path = str(schemas_traversable.joinpath('grenml.xsd'))
    schema_doc = lxml.etree.parse(schema_path)
    schema = lxml.etree.XMLSchema(schema_doc)
    return schema


class SchemaValidationError(Exception):
    """
    The methods in GRENMLParser will raise this error when the XML input
    does not conform to the GRENML schema.
    """
    pass


class GRENMLParser:
    """
    Controller to manage parsing GRENML from streams as well as files
    """

    def __init__(self):
        self.parser = xml.sax.make_parser()
        self.handler = GRENMLHandler()
        self.parser.setContentHandler(self.handler)
        self.schema = load_schema()

    def parse_byte_stream(self, byte_stream, encoding='utf-8') -> GRENMLManager:
        try:
            lxml_doc = lxml.etree.parse(byte_stream)
            self.schema.assertValid(lxml_doc)
        except lxml.etree.DocumentInvalid:
            raise SchemaValidationError()

        byte_stream.seek(0)
        self.parser.parse(TextIOWrapper(byte_stream, encoding=encoding))
        return self.handler.manager

    def parse_string(self, string) -> GRENMLManager:
        return self.parse_byte_stream(BytesIO(string.encode()))

    def parse_file(self, file_name) -> GRENMLManager:
        return self.parse_byte_stream(open(file_name, 'rb'))
