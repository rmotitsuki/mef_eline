import datetime

class Path:
    _id = None
    _endpoints = []


class Endpoint:
    _dpid = None
    _port = None
    _tag = None

    def __init__(self, dpid, port, tag=None):
        self._dpid = dpid
        self._port = port
        self._tag = tag

    @staticmethod
    def validate(data):
        if not isinstance(data, dict):
            return False
        dpid = data.get('dpid')
        port = data.get('port')
        if dpid is None or port is None:
            return False
        tag = data.get('tag')
        if tag is not None:
            if Tag.validade(tag) is False:
                return False
        return True


class Tag:
    _type = None
    _value = None

    @staticmethod
    def validate(data):
        if not isinstance(data, dict):
            return False
        type = data.get('type')
        value = data.get('value')
        if type is None or value is None:
            return False
        try:
            int(value)
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
    circuit_id = None
    name = None
    start_date = None
    end_date = None
    path = None
    backup_path = None
    uni_a = None
    uni_z = None

    def __init__(self, circuit_id=None, name=None, start_date=None,
                 end_date=None, path=None, backup_path=None, uni_a=None,
                 uni_z=None, bandwidth=None):
        self.circuit_id = circuit_id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.path = path
        self.backup_path = backup_path
        self.uni_a = uni_a
        self.uni_z = uni_z
        self.bandwidth = bandwidth

    def validate(data):
        if self.uni_a is None or self.uni_z is None or self.name is None:
            return False
        if Endpoint.validate(uni_a) is False:
            return False
        if Endpoint.validate(uni_z) is False:
            return False

        if self.path is not None:
            try:
                for link in self.path:
                    if Link.validate(link) is False:
                        return False
            except TypeError:
                return False
        if self.backup_path is not None:
            try:
                for link in backup_path:
                    if Link.validate(link) is False:
                        return False
            except TypeError:
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

