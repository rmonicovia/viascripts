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

    parent = _get(root, 'parent')

    if parent is None:
        print('<parent> node not found')
        return

    groupId = _get(parent, 'groupId')

    if groupId is None:
        print('<groupId> node not found')
        return

    if groupId.text != 'org.springframework.boot':
        print('parent.groupId is not "org.springframework.boot" (is "' + groupId.text + '")')
        return

    artifactId = _get(parent, 'artifactId')

    if artifactId is None:
        print('<artifactId> node not found')
        return

    if artifactId.text != 'spring-boot-starter-parent':
        print('parent.artifactId is not "spring-boot-starter-parent" (is "' + artifactId.text + '")')
        return

    version = parent.find('version', {'': '*'})

    if version is None:
        print('<version> node not found')
        return

    print(version.text)


if __name__ == '__main__':
    main()
