import argparse
from pydatagenerator.xml.impl import XmlParser


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="pydatagenerator")
    parser.add_argument('-i', '--input', type=str, required=True, help="Input file path")
    parser.add_argument('-o', '--output', type=str, required=True, help="Output file path")
    args = parser.parse_args()
    xml_parser = XmlParser()
    contents = xml_parser.parse_xml_from_file(args.input)
    with open(args.output, 'w+') as f:
        for item in contents:
            f.write(f'{item}\n')
