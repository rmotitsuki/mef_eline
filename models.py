from datetime import datetime
import uuid

#class Path:
#    _id = None
#    _endpoints = []
#class Link:
#    _id = None
#    _endpoint_a = None
#    _endpoint_b = None
#
#    @staticmethod
#    def validate(data):
#        if not isinstance(data, dict):
#            return False
#        endpoint_a = data.get('endpoint_a')
#        endpoint_b = data.get('endpoint_b')
#        if endpoint_a is None or endpoint_b is None:
#            return False
#        if Endpoint.validate(endpoint_a) is False:
#            return False
#        if Endpoint.validate(endpoint_b) is False:
#            return False

class Tag:
    """Class that represents a TAG, a simple UNI property."""

    def __init__(self, tag_type='VLAN', value=None):
        self.tag_type = tag_type
        self.value = value

    def is_valid(self):
        if self.tag_type not in ['VLAN', 'MPLS']:
            return False

        if not isinstance(self.value, int):
            return False

        return True

    @classmethod
    def from_dict(cls, data):
        return cls(data.get('tag_type'),
                   data.get('value'))

    def as_dict(self):
        return {"tag_type": self.tag_type,
                "value": self.value}

    def as_json(self):
        return json.dumps(self.as_dict())


class Endpoint:
    """Class that represents an endpoint according to MEF 6.2 and MEF 10.3."""

    def __init__(self, dpid, port, tag=None):
        self.dpid = str(dpid)
        self.port = str(port)
        self.tag = tag or Tag()

    def is_valid(self):
        if not isinstance(self.dpid, str):
            return False

        if not isinstance(self.port, str):
            return False

        if not isinstance(self.tag, Tag):
            return False

        return self.tag.is_valid()

    @classmethod
    def from_dict(cls, data):
        return cls(data.get('dpid'),
                   data.get('port'),
                   Tag.from_dict(data.get('tag')))

    def as_dict(self):
        return {"dpid": self.dpid,
                "port": self.port,
                "tag": self.tag.as_dict()}

    def as_json(self):
        return json.dumps(self.as_dict())


class Circuit:
    """Class that represents a circuit according to MEF 6.2 and MEF 10.3.
    
    This class has only the basics properties. We have plans to implement all
    other properties soon.
    """



    def __init__(self, name, uni_a, uni_z, start_date=None, end_date=None,
                 bandwidth=None, path=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.uni_a = uni_a
        self.uni_z = uni_z
        self.start_date = start_date or datetime.utcnow()
        self.end_date = (end_date or self.start_date +
                         datetime.timedelta(days=365))
        self.bandwidth = bandwidth
        self.path = path or []

    def is_valid(self):
        """Check if a circuit has valid properties or not."""

        if not isinstance(self.name, str):
            return False

        if not isinstance(self.uni_a, Endpoint):
            return False

        if not isinstance(self.uni_z, Endpoint):
            return False

        if not self.uni_a.is_valid():
            return False

        if not self.uni_z.is_valid():
            return False

        # Because we only support persistent VLAN tags for the service
        if self.uni_a.tag.value != self.uni_z.tag.value:
            return False

        if not isinstance(self.start_date, datetime):
            return False

        if not isinstance(self.end_date, datetime):
            return False

        if not isinstance(self.bandwidth, int):
            return False

        if not isinstance(self.path, list):
            return False

        return True

    def add_endpoint_to_path(self, endpoint):
        self.path.append(endpoint)

    @classmethod
    def from_dict(cls, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

        circuit = cls(data.get('name'),
                      Endpoint.from_dict(data['uni_a']),
                      Endpoint.from_dict(data['uni_z']),
                      start_date,
                      end_date,
                      data.get('bandwidth'))

        if not circuit.is_valid():
            raise Exception("Invalid Circuit attributes/types")

        return circuit

    def as_dict(self):
        endpoints = [ endpoint.as_dict() for endpoint in self.path ]

        return {"id": self.id,
                "name": self.name,
                "uni_a": self.uni_a.as_dict(),
                "uni_z": self.uni_z.as_dict(),
                "start_date": str(self.start_date),
                "end_date": str(self.end_date),
                "bandwidth": self.bandwidth,
                "path": endpoints}

    def as_json(self):
        return json.dumps(self.as_dict())
