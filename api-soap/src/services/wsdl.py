WSDL_TEMPLATE = '''<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="http://schemas.xmlsoap.org/wsdl/"
             xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
             xmlns:tns="http://alumno.soap.service/"
             xmlns:xsd="http://www.w3.org/2001/XMLSchema"
             name="AlumnoService"
             targetNamespace="http://alumno.soap.service/">

    <types>
        <xsd:schema targetNamespace="http://alumno.soap.service/">
            <xsd:complexType name="Alumno">
                <xsd:sequence>
                    <xsd:element name="id" type="xsd:int"/>
                    <xsd:element name="matricula" type="xsd:string"/>
                    <xsd:element name="nombre" type="xsd:string"/>
                </xsd:sequence>
            </xsd:complexType>

            <xsd:complexType name="AlumnoList">
                <xsd:sequence>
                    <xsd:element name="Alumno" type="tns:Alumno" minOccurs="0" maxOccurs="unbounded"/>
                </xsd:sequence>
            </xsd:complexType>
        </xsd:schema>
    </types>

    <!-- Messages -->
    <message name="CrearAlumnoRequest">
        <part name="nombre" type="xsd:string"/>
    </message>
    <message name="CrearAlumnoResponse">
        <part name="Alumno" type="tns:Alumno"/>
    </message>

    <message name="ObtenerAlumnoRequest">
        <part name="id" type="xsd:int"/>
    </message>
    <message name="ObtenerAlumnoResponse">
        <part name="Alumno" type="tns:Alumno"/>
    </message>

    <message name="ObtenerPorMatriculaRequest">
        <part name="matricula" type="xsd:string"/>
    </message>
    <message name="ObtenerPorMatriculaResponse">
        <part name="Alumno" type="tns:Alumno"/>
    </message>

    <message name="ListarAlumnosRequest"/>
    <message name="ListarAlumnosResponse">
        <part name="Alumnos" type="tns:AlumnoList"/>
    </message>

    <message name="ActualizarAlumnoRequest">
        <part name="id" type="xsd:int"/>
        <part name="nombre" type="xsd:string"/>
    </message>
    <message name="ActualizarAlumnoResponse">
        <part name="Alumno" type="tns:Alumno"/>
    </message>

    <message name="EliminarAlumnoRequest">
        <part name="id" type="xsd:int"/>
    </message>
    <message name="EliminarAlumnoResponse">
        <part name="message" type="xsd:string"/>
    </message>

    <!-- Port Type -->
    <portType name="AlumnoPortType">
        <operation name="CrearAlumno">
            <input message="tns:CrearAlumnoRequest"/>
            <output message="tns:CrearAlumnoResponse"/>
        </operation>
        <operation name="ObtenerAlumno">
            <input message="tns:ObtenerAlumnoRequest"/>
            <output message="tns:ObtenerAlumnoResponse"/>
        </operation>
        <operation name="ObtenerPorMatricula">
            <input message="tns:ObtenerPorMatriculaRequest"/>
            <output message="tns:ObtenerPorMatriculaResponse"/>
        </operation>
        <operation name="ListarAlumnos">
            <input message="tns:ListarAlumnosRequest"/>
            <output message="tns:ListarAlumnosResponse"/>
        </operation>
        <operation name="ActualizarAlumno">
            <input message="tns:ActualizarAlumnoRequest"/>
            <output message="tns:ActualizarAlumnoResponse"/>
        </operation>
        <operation name="EliminarAlumno">
            <input message="tns:EliminarAlumnoRequest"/>
            <output message="tns:EliminarAlumnoResponse"/>
        </operation>
    </portType>

    <!-- Binding -->
    <binding name="AlumnoBinding" type="tns:AlumnoPortType">
        <soap:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>

        <operation name="CrearAlumno">
            <soap:operation soapAction="http://alumno.soap.service/CrearAlumno"/>
            <input><soap:body use="literal"/></input>
            <output><soap:body use="literal"/></output>
        </operation>
        <operation name="ObtenerAlumno">
            <soap:operation soapAction="http://alumno.soap.service/ObtenerAlumno"/>
            <input><soap:body use="literal"/></input>
            <output><soap:body use="literal"/></output>
        </operation>
        <operation name="ObtenerPorMatricula">
            <soap:operation soapAction="http://alumno.soap.service/ObtenerPorMatricula"/>
            <input><soap:body use="literal"/></input>
            <output><soap:body use="literal"/></output>
        </operation>
        <operation name="ListarAlumnos">
            <soap:operation soapAction="http://alumno.soap.service/ListarAlumnos"/>
            <input><soap:body use="literal"/></input>
            <output><soap:body use="literal"/></output>
        </operation>
        <operation name="ActualizarAlumno">
            <soap:operation soapAction="http://alumno.soap.service/ActualizarAlumno"/>
            <input><soap:body use="literal"/></input>
            <output><soap:body use="literal"/></output>
        </operation>
        <operation name="EliminarAlumno">
            <soap:operation soapAction="http://alumno.soap.service/EliminarAlumno"/>
            <input><soap:body use="literal"/></input>
            <output><soap:body use="literal"/></output>
        </operation>
    </binding>

    <!-- Service -->
    <service name="AlumnoService">
        <port name="AlumnoPort" binding="tns:AlumnoBinding">
            <soap:address location="{service_url}"/>
        </port>
    </service>
</definitions>
'''


def get_wsdl(service_url: str) -> str:
    return WSDL_TEMPLATE.format(service_url=service_url)
