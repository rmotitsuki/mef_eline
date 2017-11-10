"""Classes used in the main application."""

import json
import uuid
from datetime import datetime

# class Path:
#     _id = None
#     _endpoints = []


class Link:
    """Define a link between two Endpoints."""

    def __init__(self, endpoint_a, endpoint_b, bandwidth):
        """Create a Link instance and set its attributes."""
        self.endpoint_a = endpoint_a
        self.endpoint_b = endpoint_b
        self.bandwidth = bandwidth

    def __eq__(self, other):
        """Check if two instances of Link are equal."""
        return (self.endpoint_a == other.endpoint_a and
                self.endpoint_b == other.endpoint_b)

    def as_dict(self):
        """Return the Link as a dictionary."""
        return {'endpoint_a': self.endpoint_a.as_dict(),
                'endpoint_b': self.endpoint_b.as_dict(),
                'bandwidth': self.bandwidth}


class Tag:
    """Class that represents a TAG, a simple UNI property."""

    def __init__(self, tag_type='VLAN', value=None):
        """Create a Tag instance and set its attributes."""
        self.tag_type = tag_type
        self.value = value

    def is_valid(self):
        """Check if a Tag has valid properties."""
        if self.tag_type not in ['VLAN', 'MPLS']:
            return False

        if not isinstance(self.value, int):
            return False

        return True

    @classmethod
    def from_dict(cls, data):
        """Create a Tag instance from a dictionary."""
        return cls(data.get('tag_type'),
                   data.get('value'))

    def as_dict(self):
        """Return the Tag as a dictionary."""
        return {"tag_type": self.tag_type,
                "value": self.value}

    def as_json(self):
        """Return the Tag as a JSON string."""
        return json.dumps(self.as_dict())


class Endpoint:
    """Class that represents an endpoint according to MEF 6.2 and MEF 10.3."""

    def __init__(self, dpid, port, tag=None):
        """Create an Endpoint instance and set its attributes."""
        self.dpid = str(dpid)
        self.port = str(port)
        self.tag = tag or Tag()

    def __eq__(self, other):
        """Check if two instances of Endpoint are equal."""
        return self.dpid == other.dpid and self.port == other.port

    def is_valid(self):
        """Check if an Endpoint has valid properties."""
        if not isinstance(self.dpid, str):
            return False

        if not isinstance(self.port, str):
            return False

        if not isinstance(self.tag, Tag):
            return False

        return self.tag.is_valid()

    @classmethod
    def from_dict(cls, data):
        """Create an Endpoint instance from a dictionary."""
        return cls(data.get('dpid'),
                   data.get('port'),
                   Tag.from_dict(data.get('tag')))

    def as_dict(self):
        """Return the Endpoint as a dictionary."""
        return {"dpid": self.dpid,
                "port": self.port,
                "tag": self.tag.as_dict()}

    def as_json(self):
        """Return the Endpoint as a JSON string."""
        return json.dumps(self.as_dict())


class Circuit:
    """Class that represents a circuit according to MEF 6.2 and MEF 10.3.

    This class has only the basics properties. We have plans to implement all
    other properties soon.
    """

    def __init__(self, name, uni_a, uni_z, start_date=None, end_date=None,
                 bandwidth=None, path=None):
        """Create a Circuit instance and set its attributes."""
        self.id = str(uuid.uuid4())
        self.name = name
        self.uni_a = uni_a
        self.uni_z = uni_z
        self.start_date = start_date or datetime.utcnow()
        self.end_date = (end_date or self.start_date +
                         datetime.timedelta(days=365))
        self.bandwidth = bandwidth
        self.path = path or []  # List of Links

    def is_valid(self):
        """Check if a Circuit has valid properties."""
        # Check basic types
        if not (isinstance(self.name, str) and isinstance(self.bandwidth, int)
                and isinstance(self.path, list)):
            return False

        # Check Endpoint instances
        if not (isinstance(self.uni_a, Endpoint) and
                isinstance(self.uni_z, Endpoint)):
            return False

        # Check datetime instances
        if not (isinstance(self.start_date, datetime) and
                isinstance(self.end_date, datetime)):
            return False

        # Perform recursive validation on Endpoints
        if not (self.uni_a.is_valid() and self.uni_z.is_valid()):
            return False

        # Because we only support persistent VLAN tags for the service
        # On the future we will support a multiple VLAN service
        if self.uni_a.tag.value != self.uni_z.tag.value:
            return False

        return True

    def add_link_to_path(self, link):
        """Add a Link to the Circuit's path."""
        self.path.append(link)

    def get_link(self, link):
        """Get a Link from the Circuit's path."""
        for path_link in self.path:
            if path_link == link:
                return path_link
        return False

    @classmethod
    def from_dict(cls, data):
        """Create a Circuit instance from a dictionary."""
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
        """Return the Circuit as a dictionary."""
        links = [link.as_dict() for link in self.path]

        return {"id": self.id,
                "name": self.name,
                "uni_a": self.uni_a.as_dict(),
                "uni_z": self.uni_z.as_dict(),
                "start_date": str(self.start_date),
                "end_date": str(self.end_date),
                "bandwidth": self.bandwidth,
                "path": links}

    def as_json(self):
        """Return the Circuit as a JSON string."""
        return json.dumps(self.as_dict())
