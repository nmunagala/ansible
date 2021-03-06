#
# (c) 2015, Peter Sprygada <psprygada@ansible.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.


class ModuleDocFragment(object):

    # Standard files documentation fragment
    DOCUMENTATION = """
options:
  host:
    description:
      - Specifies the DNS host name or address for connecting to the remote
        device over the specified transport.  The value of host is used as
        the destination address for the transport.
    required: true
  port:
    description:
      - Specifies the port to use when buiding the connection to the remote
        device.  The port value will default to the well known SSH port
        of 22
    required: false
    default: 22
  username:
    description:
      - Configures the usename to use to authenticate the connection to
        the remote device.  The value of I(username) is used to authenticate
        the SSH session. If the value is not specified in the task, the
        value of environment variable ANSIBLE_NET_USERNAME will be used instead.
    required: false
  password:
    description:
      - Specifies the password to use to authenticate the connection to
        the remote device.   The value of I(password) is used to authenticate
        the SSH session. If the value is not specified in the task, the
        value of environment variable ANSIBLE_NET_PASSWORD will be used instead.
    required: false
    default: null
  ssh_keyfile:
    description:
      - Specifies the SSH key to use to authenticate the connection to
        the remote device.   The value of I(ssh_keyfile) is the path to the
        key used to authenticate the SSH session. If the value is not specified
        in the task, the value of environment variable ANSIBLE_NET_SSH_KEYFILE
        will be used instead.
    required: false
  authorize:
    description:
      - Instructs the module to enter priviledged mode on the remote device
        before sending any commands.  If not specified, the device will
        attempt to excecute all commands in non-priviledged mode. If the value
        is not specified in the task, the value of environment variable
        ANSIBLE_NET_AUTHORIZE will be used instead.
    required: false
    default: no
    choices: ['yes', 'no']
  auth_pass:
    description:
      - Specifies the password to use if required to enter privileged mode
        on the remote device.  If I(authorize) is false, then this argument
        does nothing. If the value is not specified in the task, the value of
        environment variable ANSIBLE_NET_AUTH_PASS will be used instead.
    required: false
    default: none
  timeout:
    description:
      - Specifies idle timeout for the connection. Useful if the console
        freezes before continuing. For example when saving configurations.
    required: false
    default: 10
  provider:
    description:
      - Convience method that allows all M(ios) arguments to be passed as
        a dict object.  All constraints (required, choices, etc) must be
        met either by individual arguments or values in this dict.
    required: false
    default: null
  force:
    description:
      - The force argument instructs the module to not consider the
        current devices running-config.  When set to true, this will
        cause the module to push the contents of I(src) into the device
        without first checking if already configured.
    required: false
    default: false
    choices: ['yes', 'no']
  running_config:
    description:
      - The module, by default, will connect to the remote device and
        retrieve the current running-config to use as a base for comparing
        against the contents of source.  There are times when it is not
        desirable to have the task get the current running-config for
        every task in a playbook.  The I(config) argument allows the
        implementer to pass in the configuruation to use as the base
        config for comparision.
    required: false
    default: null
    aliases: ['config']
  save_config:
    description:
      - Specifies the current C(running-config) should be saved to
        non-volatile memory so that configuration changes are
        persistent if the device is restarted.
    required: false
    default: null
    aliases: ['save']
"""
