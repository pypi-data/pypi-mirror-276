import os
import xml.etree.ElementTree as ET


class XmlCreator:
    @staticmethod
    def create_xml_file(file_dir, file_name, **kwargs):
        root = ET.Element("root")
        # Create sub elements with the provided tags and values
        for tag, value in kwargs.items():
            element = ET.SubElement(root, tag)
            element.text = str(value)

        # Create an ElementTree object with the root element
        tree = ET.ElementTree(root)

        os.makedirs(file_dir, exist_ok=True)
        file_path = os.path.join(file_dir, file_name)

        # Write the XML content to the file
        with open(file_path, 'wb') as file:
            tree.write(file)

