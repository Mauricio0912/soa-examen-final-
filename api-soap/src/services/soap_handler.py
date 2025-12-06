from lxml import etree

SOAP_NS = 'http://schemas.xmlsoap.org/soap/envelope/'
SERVICE_NS = 'http://alumno.soap.service/'

NSMAP = {
    'soap': SOAP_NS,
    'tns': SERVICE_NS
}


def create_soap_response(body_content: etree.Element) -> str:
    envelope = etree.Element(f'{{{SOAP_NS}}}Envelope', nsmap=NSMAP)
    body = etree.SubElement(envelope, f'{{{SOAP_NS}}}Body')
    body.append(body_content)
    return etree.tostring(envelope, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode('utf-8')


def create_soap_fault(code: str, message: str) -> str:
    envelope = etree.Element(f'{{{SOAP_NS}}}Envelope', nsmap=NSMAP)
    body = etree.SubElement(envelope, f'{{{SOAP_NS}}}Body')
    fault = etree.SubElement(body, f'{{{SOAP_NS}}}Fault')

    faultcode = etree.SubElement(fault, 'faultcode')
    faultcode.text = code

    faultstring = etree.SubElement(fault, 'faultstring')
    faultstring.text = message

    return etree.tostring(envelope, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode('utf-8')


def parse_soap_request(xml_data: bytes) -> tuple[str, dict]:
    try:
        root = etree.fromstring(xml_data)
        body = root.find(f'.//{{{SOAP_NS}}}Body')

        if body is None or len(body) == 0:
            raise ValueError('Empty SOAP body')

        operation = body[0]
        operation_name = etree.QName(operation).localname

        params = {}
        for child in operation:
            param_name = etree.QName(child).localname
            if param_name == 'ids':
                ids_list = []
                for id_elem in child:
                    ids_list.append(id_elem.text)
                params[param_name] = ids_list
            else:
                params[param_name] = child.text

        return operation_name, params
    except etree.XMLSyntaxError as e:
        raise ValueError(f'Invalid XML: {e}')


def alumno_to_xml(alumno: dict, tag_name: str = 'Alumno') -> etree.Element:
    elem = etree.Element(f'{{{SERVICE_NS}}}{tag_name}')

    for key, value in alumno.items():
        child = etree.SubElement(elem, f'{{{SERVICE_NS}}}{key}')
        child.text = str(value) if value is not None else ''

    return elem


def alumnos_to_xml(alumnos: list[dict], tag_name: str = 'Alumnos') -> etree.Element:
    elem = etree.Element(f'{{{SERVICE_NS}}}{tag_name}')

    for alumno in alumnos:
        elem.append(alumno_to_xml(alumno, 'Alumno'))

    return elem


def string_response_to_xml(message: str, tag_name: str = 'Response') -> etree.Element:
    elem = etree.Element(f'{{{SERVICE_NS}}}{tag_name}')
    result = etree.SubElement(elem, f'{{{SERVICE_NS}}}message')
    result.text = message
    return elem
