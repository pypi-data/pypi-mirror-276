from lxml import etree;
from Classes.Result import *;

def XML_ValidateXSD(xml_path: str, xsd_path: str) -> Result:
    with open(xsd_path, 'r') as schema_file:
        schema = etree.XMLSchema(etree.parse(schema_file));
    with open(xml_path, 'r') as xml_file:
        doc = etree.parse(xml_file);
    try:
        schema.assertValid(doc);
        return Result(True, "XML document is valid");
    except etree.DocumentInvalid as e:
        return Result(False, f"XML document is invalid: {e}");