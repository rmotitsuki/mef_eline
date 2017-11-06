"""Main module of amlight/mef_eline Kytos Network Application.

NApp to provision circuits from user request
"""
import json
import requests
import hashlib
from sortedcontainers import SortedDict

from kytos.core import KytosNApp, log, rest
from flask import request, abort

from napps.amlight.mef_eline.models import Endpoint, Circuit
from napps.amlight.mef_eline import settings


class Main(KytosNApp):
    """Main class of amlight/mef_eline NApp.

    This class is the entry point for this napp.
    """

    def setup(self):
        """Replace the '__init__' method for the KytosNApp subclass.

        The setup method is automatically called by the controller when your
        application is loaded.

        So, if you have any setup routine, insert it here.
        """
        self._installed_circuits = {'ids': SortedDict(), 'ports': SortedDict()}
        self._pathfinder_url = settings.PATHFINDER_URL + '%s:%s/%s:%s'

    def execute(self):
        """This method is executed right after the setup method execution.

        You can also use this method in loop mode if you add to the above setup
        method a line like the following example:

            self.execute_as_loop(30)  # 30-second interval.
        """
        pass

    def shutdown(self):
        """This method is executed when your napp is unloaded.

        If you have some cleanup procedure, insert it here.
        """
        pass

    def add_circuit(self, circuit):
        self._installed_circuits['ids'][circuit._id] = circuit
        for endpoint in circuit._path:
            self._installed_circuits['ports']['%s:%s' % (endpoint._dpid, endpoint._port)] = circuit._id

    @rest('/circuit', methods=['POST'])
    def create_circuit(self):
        """
        Receive a user request to create a new circuit, find a path for the circuit,
        install the necessary flows and stores the information about it.
        :return:
        """
        data = request.get_json()

        if not isinstance(data, dict):
            abort(400)

        new_circuit = Circuit(None, data.get('name'),
                              data.get('start_date'), data.get('end_date'),
                              data.get('path'), data.get('backup_path'),
                              data.get('uni_a'), data.get('uni_b'))

        if new_circuit.validate():

            url = self._pathfinder_url % (self.uni_a['dpid'],
                                          self.uni_a['port'],
                                          self.uni_z['dpid'],
                                          self.uni_z['port'])

            log.info("Pathfinder URL: %s" % url)
            r = requests.get(url)

            if r.status_code // 100 != 2:
                log.error('Pathfinder returned error code %s.' % r.status_code)
                return json.dumps(False)
            paths = r.json()['paths']
            if len(paths) < 1:
                log.error('Pathfinder returned no path.')
                return json.dumps(False)

            path = paths[0]['hops']
            endpoints = []
            for endpoint in path:
                dpid = endpoint[:23]
                if len(endpoint) > 23:
                    port = endpoint[24:]
                    endpoints.append(Endpoint(dpid, port))

            new_circuit.path = endpoints

            m = hashlib.md5()
            m.update(uni_a['dpid'].encode('utf-8'))
            m.update(uni_a['port'].encode('utf-8'))
            m.update(uni_z['dpid'].encode('utf-8'))
            m.update(uni_z['port'].encode('utf-8'))

            new_circuit.circuit_id = m.hexdigest()

            self.add_circuit(new_circuit)
        else:
            abort(400)
        return json.dumps(circuit._id)

    @rest('/circuit/<circuit_id>', methods=['GET', 'POST', 'DELETE'])
    def circuit_operation(self, circuit_id):
        if request.method == 'GET':
            pass
        elif request.method == 'POST':
            pass
        elif request.method == 'DELETE':
            pass

    @rest('/circuits', methods=['GET'])
    def get_circuits(self):
        pass

    @rest('/circuits/byLink/<link_id>')
    def circuits_by_link(self, link_id):
        pass

    @rest('/circuits/byUNI/<dpid>/<port>')
    def circuits_by_uni(self, dpid, port):
        pass
