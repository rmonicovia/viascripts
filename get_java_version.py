#!/usr/bin/python
from xml.etree import ElementTree


def _get(node, child):
    return node.find(child, {'': '*'})


def main():
    import os

    if not os.path.exists('pom.xml'):
        print('pom.xml not found')

    with open('pom.xml') as file:
        document = ElementTree.parse(file)

    root = document.getroot()

    properties = _get(root, 'properties')

    if properties is None:
        print('<properties> node not found')
        return

    java_version = _get(properties, 'java.version')

    if java_version is None:
        maven_compiler_source = _get(properties, 'maven.compiler.source')

        if maven_compiler_source is None:
            print('Neither <java.version> nor <maven.compiler.source> nodes '
                  'was found')
            return

        java_version = maven_compiler_source

    print(java_version.text)


if __name__ == '__main__':
    main()

