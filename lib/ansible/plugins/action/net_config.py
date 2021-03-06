#
# Copyright 2015 Peter Sprygada <psprygada@ansible.com>
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
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import time
import glob
import urlparse

from ansible.plugins.action import ActionBase
from ansible.utils.unicode import to_unicode

class ActionModule(ActionBase):

    TRANSFERS_FILES = False

    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)
        result['changed'] = False

        if self._task.args.get('src'):
            try:
                self._handle_template()
            except ValueError as exc:
                return dict(failed=True, msg=exc.message)

        result.update(self._execute_module(module_name=self._task.action,
            module_args=self._task.args, task_vars=task_vars))

        if self._task.args.get('backup_config') and result.get('__backup__'):
            # User requested backup and no error occurred in module.
            # NOTE: If there is a parameter error, _backup key may not be in results.
            self._write_backup(task_vars['inventory_hostname'], result['__backup__'])

        if self._task.args.get('dest') and result.get('__config__'):
            self._write_dest(self._task.args['dest'], result['__config__'],
                             append=self._task.args['append'])

        for key in ['__config__', '__backup__']:
            if key in result:
                del result[key]

        return result

    def _get_working_path(self):
        cwd = self._loader.get_basedir()
        if self._task._role is not None:
            cwd = self._task._role._role_path
        return cwd

    def _write_backup(self, host, contents):
        backup_path = self._get_working_path() + '/backup'
        if not os.path.exists(backup_path):
            os.mkdir(backup_path)
        for fn in glob.glob('%s/%s*' % (backup_path, host)):
            os.remove(fn)
        tstamp = time.strftime("%Y-%m-%d@%H:%M:%S", time.localtime(time.time()))
        filename = '%s/%s_config.%s' % (backup_path, host, tstamp)
        open(filename, 'w').write(contents)

    def _write_dest(self, path, contents, append=False):
        dirpath = os.path.dirname(path)
        if not dirpath[0] == '/':
            dirpath = self._get_working_path() + dirpath
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        if append:
            flags = 'a'
        else:
            flags = 'w'
        open(path, flags).write(contents)

    def _handle_template(self):
        src = self._task.args.get('src')
        working_path = self._get_working_path()

        if os.path.isabs(src) or urlparse.urlsplit('src').scheme:
            source = src
        else:
            source = self._loader.path_dwim_relative(working_path, 'templates', src)
            if not source:
                source = self._loader.path_dwim_relative(working_path, src)

        if not os.path.exists(source):
            return

        try:
            with open(source, 'r') as f:
                template_data = to_unicode(f.read())
        except IOError:
            return dict(failed=True, msg='unable to load src file')

        # Create a template search path in the following order:
        # [working_path, self_role_path, dependent_role_paths, dirname(source)]
        searchpath = [working_path]
        if self._task._role is not None:
            searchpath.append(self._task._role._role_path)
            dep_chain = self._task._block.get_dep_chain()
            if dep_chain is not None:
                for role in dep_chain:
                    searchpath.append(role._role_path)
        searchpath.append(os.path.dirname(source))
        self._templar.environment.loader.searchpath = searchpath
        self._task.args['src'] = self._templar.template(template_data)


