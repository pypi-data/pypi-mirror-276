# -*- coding: utf-8 -*-

def example_1():
    """Simple"""

    import a2dl.a2dl

    # Create a library
    DL = a2dl.a2dl.Diaglibrary()
    # DL.image_base_path = 'src/img'  #if images are located elsewhere
    DL.from_folder('./data/docs')
    DL.write('./test/test-generated-library.xml')

    #  Update a diagram
    DG = a2dl.a2dl.Diagdiagram()
    DG.from_file('./test/exampleDiagramFromLibrary-old.drawio')
    DG.update(libraries=[DL])


def example_2():
    """Customize"""

    import a2dl.core.constants

    # Overwrite some constants
    a2dl.core.constants.ICON_STYLE = "rounded=1;whiteSpace=wrap;html=1;"
    a2dl.core.constants.IMAGE_STYLE = 'fillColor=none;rounded=1;shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/{},{};'

    import a2dl.a2dl

    a2dl.a2dl.logging.getLogger('a2dl').addHandler(a2dl.a2dl.logging.NullHandler())

    # create icon
    DI = a2dl.a2dl.Diagicon()
    DI.from_adoc('./data/examples/docs/exampleDocument.adoc')
    # write the icon to a Diagram file
    DI.write_diagram('./test/test-generated-icon-from-exampleDocument.drawio')

    # create a library
    DL = a2dl.a2dl.Diaglibrary()
    DL.from_folder('./data/examples/docs')
    DL.write('./test/test-generated-library.xml')

    #  update a diagram
    DG = a2dl.a2dl.Diagdiagram()
    DG.from_file('./data/examples/dio/exampleDiagramFromLibrary-old.drawio')
    DG.update(libraries=[DL])


def extras():
    import a2dl.a2dl

    # a2dl.a2dl.logging.getLogger('a2dl').addHandler(a2dl.a2dl.logging.NullHandler())
    a2dl.a2dl.logger.setLevel("DEBUG")

    print(a2dl.a2dl.my_environment())
    print(a2dl.a2dl.make_utf8('./data/examples/docs/exampleDocument.adoc'))


def dev_test():
    import a2dl.a2dl as librarian

    print(librarian.my_environment())
    print(librarian.make_utf8('./data/examples/docs/exampleDocument.adoc'))

    # create icon
    DI = librarian.Diagicon()
    DI.from_adoc('./data/examples/docs/exampleDocument.adoc')
    # write the icon to a Diagram file
    DI.write_diagram('./test/test-generated-icon-from-exampleDocument.drawio')

    # create a library
    DL = librarian.Diaglibrary()
    DL.from_folder('./data/examples/docs')
    DL.write('./test/test-generated-library.xml')

    #  update a diagram
    DG = librarian.Diagdiagram()
    DG.from_file('./data/examples/dio/exampleDiagramFromLibrary-old.drawio')
    DG.update(libraries=[DL])

    # # create examples
    # a2dl.a2dl.make_example('./test/plain_example')

    librarian.to_pptx(DL, './test/test-generated-library.pptx',
                      whitelist=['xml_attribute_1', 'xml_attribute_2'])
    librarian.to_docx(DL, './test/test-generated-library.docx',
                      whitelist=['xml_attribute_1', 'xml_attribute_2'])

    # librarian.to_ea(DL, './test/test-generated-library.ea')

    # create a graph network diagram of library icons
    # list of tuples with each:
    #      0 - Source Icon Name,
    #      1 - Target Icon Name,
    #      2 - True/False for arrow on a connection,
    #      3 - List of Labels to show on the connection
    #      4 - For the text generator, additional context
    IRL = [
        ('IconOverview', 'Example', False, ['implements']),
        ('IconOverview', 'UnknownIcon', False, ['uses']),
        ('byCode', 'IconOverview', True, ['know each other']),
        ('UnknownIcon', 'byCode', False, ['depends']),
    ]
    # make a graph
    IR = librarian.IconRelations()
    IR.set(IRL, libraries=[DL])
    IR.write_diagram('./test/test-generated-diagram-from-graph-data.drawio')

    # #  ai generate
    # IRL2 = [
    #     ('Equalization', 'Compression', False, ['influences'], '', ''),
    #     ('Compression', 'Limiting', False, ['can lead to'], '', 'is a method of reducing the dynamic range of music. '),
    #     ('Limiting', 'Equalization', True, ['is influenced by'], 'When we talk about',
    #      ',in the sense of Music creation and audio engineering then we refer to'),
    #     ('Spatialization', 'Equalization', False, ['depends'],
    #      'Bei der Produktion von Audiomaterial können Schallereignisse akustisch im Raum verortet werden. Dabei spricht man von',
    #      ''),
    # ]
    #
    # pre = 'In the Context Audio Engineering, Mastering, Music and Sound, the Term'
    # post = 'is defined as'
    # a2dl.a2dl.feed(IRL2, pre, post, target='./test')
