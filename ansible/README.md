# Discord Ansible

## Required

- Vagrant (ローカル確認用)
    - Dockerでも試そうと思えば試せますが、色々実際のサーバーと異なるため、Vagrantを使用
- Ansible 3.8.2 or later

# Get started

```sh
# project rootで実行
$ vagrant up

# ssh用の情報を追記
$ vagrant ssh-config --host=discord-local >> ~/.ssh/config

$ cd ansible
$ ansible-playbook -i inventories/local/hosts site.yml
```
