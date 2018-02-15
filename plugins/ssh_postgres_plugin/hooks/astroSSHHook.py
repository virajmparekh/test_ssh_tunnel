# -*- coding: utf-8 -*-
#
# Copyright 2012-2015 Spotify AB
# Ported to Airflow by Bolke de Bruin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import getpass
import os
import stat
import shlex
from airflow.models import Variable
from airflow.hooks.base_hook import BaseHook
import logging
import getpass
import os
import socket
import select
try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer


class AstroSSHHook(BaseHook):

    def __init__(
            self,
            ssh_conn_id):
        self.ssh_conn_id = ssh_conn_id

        super().__init__(ssh_conn_id)

    def create_tunnel(self):
        """
        Creates a tunnel between two hosts. Like ssh -L <LOCAL_PORT>:host:<REMOTE_PORT>.
        Hard coded in for now. Down the line, it will pull from connections panel.

        """
        import subprocess

        localport = '5439'
        remoteport = '5439'
        user = 'ubuntu'
        server = '54.236.32.199'
        incoming_port = 17386
        key = Variable.get("key_file")
        identityfile = 'key_file.pem'

        # Write the key to a file to change permissions
        # The container dies after the task executes, so don't have to
        # worry about closing/deleting it.
        with open("key_file.pem", "w") as key_file:
            key_file.write(key)

        print(os.listdir())


        os.chmod("key_file.pem", stat.S_IRWXU)

        # SSH is a black box that no one wants to touch.

        sshTunnelCmd = """ssh -4 -i {identityfile} -L  {localhost}:10.20.2.111:{remote_port} -tt -o ExitOnForwardFailure=yes -o "StrictHostKeyChecking no" {user}@{server}""".format(
            localhost=localport,
            remote_port=remoteport,
            identityfile=identityfile,
            user=user,
            server=server
        )
        print(sshTunnelCmd)
        logging.info(sshTunnelCmd)

        args = shlex.split(sshTunnelCmd)
        print("MAKING TUNNEL!")
        tunnel = subprocess.Popen(args)
