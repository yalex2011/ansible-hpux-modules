#!/usr/bin/python

# Copyright: (c) 2020, yalex2011 <yalex@example.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: hpux_pass

short_description: This is my HP-UX password module

version_added: "1.0"

description:
    - "Preparing an encrypted password for HP-UX"

options:
    password:
        description:
            - This is not an encrypted password passed to the module.
        required: true


author:
    - Alexey Yushkov (@yalex2011)
'''

EXAMPLES = '''
# 
    - local_action:
        module: hpux_pass
        password: "password"
      no_log: true
      register: pwd
'''

RETURN = '''
original_password:
    description: The original param that was passed in module
    type: str
    returned: always
password:
    description: The output param that the module generates
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule

from passlib.hash import des_crypt

def run_module():

    module_args = dict(
        password=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        original_password='',
        password=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    result['original_password'] = module.params['password']
    result['password'] = des_crypt.using(salt='xy').hash(module.params['password'])

    if result['original_password'] != result['password']:
        result['changed'] = True

    if module.params['password'] == '':
        module.fail_json(msg='You requested this to fail', **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
