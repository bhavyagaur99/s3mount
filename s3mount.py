#!/usr/bin/python3

import argparse
import stat
import input
import os
import shelve
import json

cwd = os.getcwd()
data_path = os.path.join(cwd, 'data')
shelve_file = os.path.join(data_path, 'mounts.store')

try:
    os.makedirs(data_path)
except:
    pass

create_help = "Create a new s3fs config"
delete_help = "Delete a s3fs config"
display_help = "List all s3fs config: -l all to list all | -l <name> to list one"
mount_help = "Mount a s3fs config"
unmount_help = "Unmount a s3fs config"


def create(m):
    opt = dict()
    opt['config_name'] = input.get_string(start='name of config >>> ', min_len=3, max_len=32, print_value=True)
    opt['key_id'] = input.get_string(start='key id >>> ', min_len=3, max_len=200, print_value=True)
    opt['key_secret'] = input.get_string(start='key secret >>> ', min_len=3, max_len=200, print_value=True)
    opt['bucket_name'] = input.get_string(start='bucket name >>> ', min_len=3, max_len=200, print_value=True)
    opt['mount_path'] = input.get_string(start='mount path >>> ', min_len=3, max_len=255, print_value=True)
    opt['endpoint'] = input.get_string(start='endpoint >>> ', min_len=3, max_len=1024, print_value=True)

    with shelve.open(shelve_file, writeback=True) as db:
        db[opt['config_name']] = opt

    passwd_file = os.path.join(data_path, opt['config_name'] + '.cred')
    print('making password file:', passwd_file)
    with open(passwd_file, 'w') as file:
        file.write(f'{opt["key_id"]}:{opt["key_secret"]}')

    print('updating file permission')
    os.chmod(passwd_file, stat.S_IREAD)
    os.system(f'ls -al {passwd_file}')

    try:
        os.makedirs(opt['mount_path'])
        print('created:', opt['mount_path'])
    except:
        print('path already present')


def delete(m_list):
    with shelve.open(shelve_file, writeback=True) as db:
        for m in m_list:
            try:
                del db[m]
                print(m, "deleted")
            except:
                print(m, 'does not exist')


def display(m_list):
    with shelve.open(shelve_file) as db:
        if len(m_list) == 1 and m_list[0] == 'all':
            for v in db.values():
                print(json.dumps(v, indent=4))
        else:
            for m in m_list:
                try:
                    print(json.dumps(db[m], indent=4))
                except:
                    print(m, 'does not exist')


def mount(m_list):
    if os.geteuid() != 0:
        print('this action requires sudo privileges')
        exit(1)

    with shelve.open(shelve_file) as db:
        for m in m_list:
            try:
                opt = db[m]
                passwd_file = os.path.join(data_path, opt['config_name'] + '.cred')
                cmd = f's3fs {opt["bucket_name"]} {opt["mount_path"]}' \
                      f' -o passwd_file={passwd_file}' \
                      f' -o url={opt["endpoint"]}' \
                      f' -o use_path_request_style'
                print('cmd:', cmd)
                os.system(cmd)

            except Exception as e:
                print('err:', e)


def unmount(m_list):
    if os.geteuid() != 0:
        print('this action requires sudo privileges')
        exit(1)

    with shelve.open(shelve_file) as db:
        for m in m_list:
            try:
                opt = db[m]
                os.system(f'umount -l {opt["mount_path"]}')
            except Exception as e:
                print('err:', e)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--create-config', '-c', help=create_help, dest='create', action='store_true')
    ap.add_argument('--delete-config', '-d', help=delete_help, action='append', dest='delete')
    ap.add_argument('--list-config', '-l', help=display_help, dest='display', action='append')
    ap.add_argument('--mount-config', '-m', help=mount_help, action='append', dest='mount')
    ap.add_argument('--unmount-config', '-u', help=unmount_help, action='append', dest='unmount')
    args = ap.parse_args()

    if args.create:
        create(getattr(args, 'create'))
    elif args.delete:
        delete(getattr(args, 'delete'))
    elif args.display:
        display(getattr(args, 'display'))
    elif args.mount:
        mount(getattr(args, 'mount'))
    elif args.unmount:
        unmount(getattr(args, 'unmount'))
    else:
        print('Unknown operation exiting')
