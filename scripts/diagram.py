"""
System architecture diagram creation
"""
from diagrams import Diagram
from diagrams.c4 import Container, Database, System, SystemBoundary, Relationship

graph_attr = {
    'splines': 'spline'
}

with Diagram('MaxPayload Data Processing Architecture', graph_attr=graph_attr):
    third_party = System(
            name='Third-Pary API',
            description='Various third-party APIs used to support Maxpayload'
    )
    
    with SystemBoundary('MaxPayload Internal'):
        microservice = Container(
            name='Microservice',
            technology="Django",
            description=('Microservice designed to poll external systems for new data, '
                         'or receive webooks. Responsible for denormalization and '
                         'writing to s3. May be part of webserver, but logically isolated.')
        )
        s3 = Container(
            name='s3',
            technology='AWS s3 cloud storage',
            description=('Storage of third-party datasets for later ingestion '
                         'into Snowflake or other DBs as needed. Should store unprocessed '
                         'and denormalized data as failsafe')
        )
        snowflake = Container(
            name='Snowflake',
            technology='Snowflake Data Warehouse',
            description=('Primary storage for denormlaized report data. '
                         'Data may be auto-ingested through Tasks or Snowpipe '
                         'depending on requirements ')
        )
        api = Container(
            name='Internal API',
            technology='Django',
            description=('Logical access layer for data stored in Snowflake. '
                        'Provides interface to database, serialization, etc')
        )
    
    frontend = System(
        name="MaxPayload Frontend",
        technology="Next.JS",
        description="UI for arbitrary report generation. Communicates with Internal API"
    )

    third_party >> Relationship(
        'Data received via webhook or through polling third-pary'
        ) >> microservice
    microservice >> Relationship(
        'Denormalized data written to s3 for later ingestion to Snowflake'
        ) >> s3
    s3 >> Relationship(
        'Denormalized data available in Snowflake'
        ) >> snowflake
    snowflake << Relationship(
        'Webserver queries Snowflake based on user-defined reports'
        ) >> api
    api << Relationship(
        'Frontend requests report from webserver, webserver responds'
        ) >> frontend