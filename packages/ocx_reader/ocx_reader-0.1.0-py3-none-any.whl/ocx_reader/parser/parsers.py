#  Copyright (c) 2023. OCX Consortium https://3docx.org. See the LICENSE
"""Module for parsing a 3Docx model."""

# system imports
from abc import ABC
from dataclasses import dataclass
from typing import Dict
from enum import Enum

# 3rd party imports
import lxml.etree
from loguru import logger
from lxml.etree import Element
from xsdata.exceptions import ParserError
from xsdata.formats.dataclass.context import XmlContext, XmlContextError
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.parsers.handlers import LxmlEventHandler

# Project imports
from ocx_common.interfaces import (IObservable)
from ocx_common.utilities import SourceValidator, OcxXml, SourceError
from ocx_reader.loader.loader import DeclarationOfOcxImport, DynamicLoader


class OcxParserError(ParserError):
    """Errors raised by this module."""


class ObservableEvent(Enum):
    """Events that can be listened to and broadcast."""
    DATACLASS = 'dataclass'
    REPORT = 'report'
    SERIALIZE = 'serialize'


class XmlParserError(ValueError):
    """Parser errors."""


class MetaData:
    """Dataclass metadata."""

    @staticmethod
    def meta_class_fields(data_class: dataclass) -> Dict:
        """
        Return the dataclass metadata.

        Args:
            data_class: The dataclass instance

        Returns:
            The metadata of the class
        """
        return dict(data_class.Meta.__dict__.items())

    @staticmethod
    def class_name(data_class: dataclass) -> str:
        """Return the name of the class"""
        declaration = str(data_class.__class__)
        return declaration[declaration.rfind(".") + 1: -2]

    @staticmethod
    def namespace(data_class: dataclass) -> str:
        """Get the OCX namespace

        Args:
            data_class: The dataclass instance

        Returns:
            The namespace of the dataclass
        """
        return MetaData.meta_class_fields(data_class).get("namespace")

    @staticmethod
    def name(data_class: dataclass) -> str:
        """Get the OCX name

        Args:
            data_class: The dataclass instance

        Returns:
            The name of the OCX type
        """
        return MetaData.meta_class_fields(data_class).get("name")


class OcxNotifyParser(IObservable, ABC):
    """Ocx notification parser class for 3Docx XML files.

     Args:
         fail_on_unknown_properties: Don't bail out on unknown properties.
         fail_on_unknown_attributes: Don't bail out on unknown attributes
         fail_on_converter_warnings: bool = Convert warnings to exceptions

     """

    def __init__(
            self,
            fail_on_unknown_properties: bool = False,
            fail_on_unknown_attributes: bool = False,
            fail_on_converter_warnings: bool = True,
    ):
        context = XmlContext()
        parser_config = ParserConfig(
            fail_on_unknown_properties=fail_on_unknown_properties,
            fail_on_unknown_attributes=fail_on_unknown_attributes,
            fail_on_converter_warnings=fail_on_converter_warnings,
            class_factory=self.class_factory)
        self._parser = XmlParser(config=parser_config, context=context)
        self._subscribers = set()

    def subscribe(self, observer):
        self._subscribers.add(observer)
        return

    def unsubscribe(self, observer):
        self._subscribers.remove(observer)
        return

    def update(self, event: ObservableEvent, payload: Dict):
        for observer in self._subscribers:
            observer.update(event, payload)

    def class_factory(self, clazz, params):
        """Custom class factory method"""
        name = clazz.__name__
        new_data_class = clazz(**params)
        # Broadcast an update
        namespace = MetaData.namespace(clazz)
        # name = MetaData.name(clazz)
        fields = MetaData.meta_class_fields(clazz)
        logger.debug(f'Meta fields: {fields}')
        tag = '{' + namespace + '}' + name
        self.update(ObservableEvent.DATACLASS, {'name': tag, 'object': new_data_class})
        return new_data_class

    def parse(self, xml_file: str) -> dataclass:
        """Parse a 3Docx XML model and return the root dataclass.

        Args:
            xml_file: The 3Docx xml file or url to parse.

        Returns:
            The root dataclass instance of the parsed 3Docx XML.
        """
        try:
            file_path = SourceValidator.validate(xml_file)
            tree = lxml.etree.parse(xml_file)
            root = tree.getroot()
            version = OcxXml.get_version(file_path)
            declaration = DeclarationOfOcxImport("ocx", version)
            # Load target schema version module
            ocx_module = DynamicLoader.import_module(declaration)
            return self._parser.parse(root, ocx_module.OcxXml)
        except lxml.etree.XMLSyntaxError as e:
            logger.error(e)
            raise XmlParserError(e) from e
        except ImportError as e:
            logger.error(e)
            raise XmlParserError from e
        except XmlContextError as e:
            logger.error(e)
            raise XmlParserError from e
        except ParserError as e:
            logger.error(e)
            raise XmlParserError from e

    def parse_element(self, element: Element, ocx_module) -> dataclass:
        """Parse a 3Docx XML element and return the dataclass.

        Args:
            element: The 3Docx XML Element to parse.

        Returns:
            The element dataclass instance.
        """
        try:
            return self._parser.parse(element, ocx_module)
        except lxml.etree.XMLSyntaxError as e:
            logger.error(e)
            raise XmlParserError(e) from e
        except ImportError as e:
            logger.error(e)
            raise XmlParserError from e
        except XmlContextError as e:
            logger.error(e)
            raise XmlParserError from e
        except ParserError as e:
            logger.error(e)
            raise XmlParserError from e


class OcxParser:
    """OcxParser class for 3Docx XML files.

    Args:
        ocx_model: The file path or URL to the source model.

    """

    def __init__(
            self, ocx_model: str, ):
        self._parser = XmlParser(handler=LxmlEventHandler)
        self._tree: lxml.etree = None
        self._version: str = ''
        try:
            file = SourceValidator.validate(ocx_model)
            self._version = OcxXml.get_version(file)
            self._tree = lxml.etree.parse(file)
        except SourceError as e:
            logger.error(e)
            raise OcxParserError(e) from e
        except ParserError as e:
            logger.error(e)
            raise OcxParserError(e) from e
