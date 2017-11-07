import datetime


class Path:
    _id = None
    _endpoints = []


class Endpoint:

    def __init__(self, dpid=None, port=None, tag=None):
        self.dpid = dpid
        self.port = port
        self.tag = Tag(tag)

    def validate(self):
        if self.dpid is None or self.port is None:
            return False
        if tag is not None:
            if self.tag.validade() is False:
                return False
        return True


class Tag:

    def __init__(self, tag_type=None, value=None):
        self.tag_type = tag_type
        self.value = value

    def validate(data):
        if self.tag_type is None or self.value is None:
            return False
        try:
            int(self.value)
        except TypeError:
            return False
        return True


class Link:
    _id = None
    _endpoint_a = None
    _endpoint_b = None

    @staticmethod
    def validate(data):
        if not isinstance(data, dict):
            return False
        endpoint_a = data.get('endpoint_a')
        endpoint_b = data.get('endpoint_b')
        if endpoint_a is None or endpoint_b is None:
            return False
        if Endpoint.validate(endpoint_a) is False:
            return False
        if Endpoint.validate(endpoint_b) is False:
            return False


class Circuit:

    def __init__(self, uni_a=None, uni_z=None, path=None, start_date=None,
                 end_date=None, bandwidth=None):

        self.start_date = start_date
        self.end_date = end_date
        self.path = path or []
        self.uni_a = Endpoint(uni_a)
        self.uni_z = Endpoint(uni_z)
        self.bandwidth = bandwidth

    def validate(self):
        if self.uni_a.validate() is False:
            return False
        if self.uni_z.validate() is False:
            return False

        if self.start_date is not None:
            try:
                datetime.datetime.strptime(self.start_date,
                                           '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return False
        if self.end_date is not None:
            try:
                datetime.datetime.strptime(self.end_date, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return False

        if self.bandwidth is not None:
            try:
                int(self.bandwidth)
            except TypeError:
                return False
        return True
