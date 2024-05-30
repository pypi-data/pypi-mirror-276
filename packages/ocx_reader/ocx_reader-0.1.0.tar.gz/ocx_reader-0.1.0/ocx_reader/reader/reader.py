#  Copyright (c) 2024. OCX Consortium https://3docx.org. See the LICENSE

# system imports
from enum import Enum
from typing import List, Any

# Third party imports

from loguru import logger
# Project imports
from ocx_common.utilities import OcxXml
from ocx_reader.parser.parsers import OcxParser, MetaData
from ocx_reader.loader.loader import DeclarationOfOcxImport, DynamicLoader, DynamicLoaderError
from ocx_schema_parser.xelement import LxmlElement


class OcxReaderError(ValueError):
    """ Reader error class"""


class OCXPythonType(Enum):
    ROOT: Enum = 'OcxXml'
    HEADER: Enum = 'Header'
    PANEL: str = 'Panel'
    PLATE: str = 'Plate'
    BRACKET: str = 'Bracket'
    STIFFENER: str = 'Stiffener'
    PILLAR: str = 'Pillar'
    XREF_PLANES: str = 'XrefPlanes'
    YREF_PLANES: str = 'YrefPlanes'
    ZREF_PLANES: str = 'ZrefPlanes'
    REFERENCE_SURFACES: str = 'ReferenceSurfaces'
    UNITSET: str = 'UnitSet'
    MATERIAL_CATALOGUE: str = 'MaterialCatalogue'
    SECTION_CATALOGUE: str = 'XsectionCatalogue'
    HOLE_CATALOGUE: str = 'HoleShapeCatalogue'
    PRINCIPAL_PARTICULARS: str = 'PrincipalParticulars'


class OcxReader(OcxParser):
    def __init__(self, ocx_model: str, ):
        """Defines a class for reading OCX elements and root from an OCX model."""
        super().__init__(ocx_model)

    def read_ocx_element(self, ocx_element: OCXPythonType, ) -> List[Any]:
        """
        Reads a specific OCX element and returns a list of parsed elements.

        Args:
        - ocx_element: The type of OCX element to read.

        Returns:
        - List[Any]: A list of parsed elements.

        Raises:
        - OcxReaderError: If an error occurs during the reading process.
        """

        try:
            root = self._tree.getroot()
            declaration = DeclarationOfOcxImport("ocx", self._version)
            data_class = DynamicLoader.import_class(declaration, ocx_element.value)
            result = []
            logger.info(f'Parsing object {data_class!r}')
            xml_name = MetaData.name(data_class)
            if xml_name is None:
                xml_name = ocx_element.value
            for e in LxmlElement.find_all_children_with_name(root, xml_name):
                ocx_element = self._parser.parse(e, data_class)
                result.append(ocx_element)
            if result:
                logger.info(f'Created  {len(result)!r} of type {ocx_element!r}')
            return result
        except DynamicLoaderError as e:
            logger.error(e)
            raise OcxReaderError(e) from e

    def read_ocx_root(self, ) -> OcxXml:
        """
        Reads the root element of the OCX model and returns the parsed element.

        Returns:
        - OcxXml: The parsed root element.

        Raises:
        - OcxReaderError: If an error occurs during the reading process.
        """
        try:
            root = self._tree.getroot()
            declaration = DeclarationOfOcxImport("ocx", self._version)
            data_class = DynamicLoader.import_class(declaration, 'OcxXml')
            logger.info(f'Parsing object {data_class!r}')
            ocx_element = self._parser.parse(root, data_class)
            return ocx_element
        except DynamicLoaderError as e:
            logger.error(e)
            raise OcxReaderError(e) from e

    def read_header(self, ) -> List[Any]:
        """
        Reads and returns a list of Header elements.

        Returns:
        - List[Any]: A list of parsed Header elements.
        """
        return self.read_ocx_element(OCXPythonType.HEADER)

    def read_unit_set(self, ) -> List[Any]:
        """
        Reads and returns a list of UnitSet elements.

        Returns:
        - List[Any]: A list of parsed UnitSet elements.
        """

        return self.read_ocx_element(OCXPythonType.UNITSET)

    def read_principal_particulars(self, ) -> List[Any]:
        """
        Reads and returns a list of PrincipalParticulars elements.

        Returns:
        - List[Any]: A list of parsed PrincipalParticulars elements.
        """

        return self.read_ocx_element(OCXPythonType.PRINCIPAL_PARTICULARS)

    def read_panels(self, ) -> List[Any]:
        """
        Reads and returns a list of Panel elements.

        Returns:
        - List[Any]: A list of parsed Panel elements.
        """

        return self.read_ocx_element(OCXPythonType.PANEL)

    def read_plates(self, ) -> List[Any]:
        """
        Reads and returns a list of Plate elements.

        Returns:
        - List[Any]: A list of parsed Plate elements.
        """

        return self.read_ocx_element(OCXPythonType.PLATE)

    def read_brackets(self, ) -> List[Any]:
        """
        Reads and returns a list of Bracket elements.

        Returns:
        - List[Any]: A list of parsed Bracket elements.
        """

        return self.read_ocx_element(OCXPythonType.BRACKET)

    def read_stiffeners(self, ) -> List[Any]:
        """
        Reads and returns a list of Stiffener elements.

        Returns:
        - List[Any]: A list of parsed Stiffener elements.
        """

        return self.read_ocx_element(OCXPythonType.STIFFENER)

    def read_pillars(self, ) -> List[Any]:
        """
        Reads and returns a list of Pillar elements.

        Returns:
        - List[Any]: A list of parsed Pillar elements.
        """

        return self.read_ocx_element(OCXPythonType.PILLAR)

    def read_material_catalogue(self, ) -> List[Any]:
        """
        Reads and returns a list of MaterialCatalogue elements.

        Returns:
        - List[Any]: A list of parsed MaterialCatalogue elements.
        """

        return self.read_ocx_element(OCXPythonType.MATERIAL_CATALOGUE)

    def read_section_catalogue(self, ) -> List[Any]:
        """
        Reads and returns a list of XsectionCatalogue elements.

        Returns:
        - List[Any]: A list of parsed XsectionCatalogue elements.
        """

        return self.read_ocx_element(OCXPythonType.SECTION_CATALOGUE)

    def read_hole_shape_catalogue(self, ) -> List[Any]:
        """
        Reads and returns a list of HoleShapeCatalogue elements.

        Returns:
        - List[Any]: A list of parsed HoleShapeCatalogue elements.
        """

        return self.read_ocx_element(OCXPythonType.HOLE_CATALOGUE)

    def read_x_ref_planes(self, ) -> List[Any]:
        """
        Reads and returns a list of XrefPlanes elements.

        Returns:
        - List[Any]: A list of parsed XrefPlanes elements.
        """

        return self.read_ocx_element(OCXPythonType.XREF_PLANES)

    def read_y_ref_planes(self, ) -> List[Any]:
        """
        Reads and returns a list of YrefPlanes elements.

        Returns:
        - List[Any]: A list of parsed YrefPlanes elements.
        """

        return self.read_ocx_element(OCXPythonType.YREF_PLANES)

    def read_z_ref_planes(self, ) -> List[Any]:
        """
        Reads and returns a list of ZrefPlanes elements.

        Returns:
        - List[Any]: A list of parsed ZrefPlanes elements.
        """

        return self.read_ocx_element(OCXPythonType.ZREF_PLANES)

    def read_reference_surfaces(self, ) -> List[Any]:
        """
        Reads and returns a list of ReferenceSurfaces elements.

        Returns:
        - List[Any]: A list of parsed ReferenceSurfaces elements.
        """

        return self.read_ocx_element(OCXPythonType.REFERENCE_SURFACES)
