```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
import sys

MAP = {
    'a': ("apt", [['apt', 'update'], ['apt', 'full-upgrade', '-y']]),
    'd': ("dnf", [['dnf', 'upgrade', '--refresh', '-y']]),
    'p': ("pacman", [['pacman', '-Syu', '--noconfirm']]),
    'z': ("zypper", [['zypper', 'refresh'], ['zypper', 'update', '-y']]),
    'f': ("flatpak", [['flatpak', 'update', '-y']]),
    's': ("snap", [['snap', 'refresh']]),
    'x': ("auto", None),
}

PREF_ORDER = ['a', 'd', 'p', 'z', 'f', 's']

def detect_manager():
    for key in PREF_ORDER:
        name = MAP[key][0]
        # check common executable names
        exe = {
            'a': 'apt-get',
            'd': 'dnf',
            'p': 'pacman',
            'z': 'zypper',
            'f': 'flatpak',
            's': 'snap'
        }.get(key)
        if exe and shutil.which(exe):
            return key
    return None

def run_commands(cmds):
    is_root = (os.geteuid() == 0)
    for cmd in cmds:
        full = cmd[:]  # copy
        if not is_root:
            full.insert(0, 'sudo')
        print("Executando:", " ".join(full))
        try:
            subprocess.run(full, check=True)
        except subprocess.CalledProcessError as e:
            print("Falha ao executar:", " ".join(full), file=sys.stderr)
            return False
    return True

def main():
    print("Atualizador rápido — pressione uma letra e Enter:")
    print(" a=apt  d=dnf  p=pacman  z=zypper  f=flatpak  s=snap  x=auto-detect")
    choice = input("> ").strip().lower()[:1]
    if choice not in MAP:
        print("Escolha inválida.")
        sys.exit(1)

    if choice == 'x':
        choice = detect_manager()
        if not choice:
            print("Nenhum gerenciador de pacotes detectado.")
            sys.exit(1)
        print("Detectado:", MAP[choice][0])

    name, cmds = MAP[choice]
    if cmds is None:
        print("Sem comandos configurados para:", name)
        sys.exit(1)

    ok = run_commands(cmds)
    if ok:
        print("Atualização concluída com sucesso.")
    else:
        print("A atualização encontrou erros.", file=sys.stderr)
        sys.exit(2)

if __name__ == '__main__':
    main()