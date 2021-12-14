# A script that simplify mvm publishment
#
# Requirements: 
#
# 1. Unix system
#
# 2. mixin-cli and mvm downloaded
# (https://github.com/fox-one/mixin-cli)
# (https://github.com/MixinNetwork/trusted-group)
#
#
# Get Started:
#
# 0. Change mixincliPATH, botConfigPATH, mvmPATH, mvmCONF to your own.
#    - mixincliPATH:  PATH of mixin-cli
#    - botConfigPATH: PATH of your mixin bot
#    - mvmPATH:       PATH of mvm
#    - mvmCONF:       PATH of mvm config (config.toml)
#   
# 1. python3 mvm.py new
#
# 2. Edit and publish contract in remix
#
# 3. python3 mvm.py publish [ADDRESS] [TX HASH]

import os
import json
from sys import argv


mixincliPATH   = "./mixin-cli"
botConfigPATH  = "../../trusted-group/mvm/7000104232.json"
mvmPATH        = "../../trusted-group/mvm/mvm"
mvmCONF        = "../../trusted-group/mvm/config.toml"

newNetUsername = "dumbass"
newNetUserFile = "dumbass.json"
cnbUUID        = "965e5c6e-434c-3fa9-b780-c50f43cd955c"
cnbAMOUNT      = "10"

# New Net User
if len(argv)==1:
    print("""
Simplify mvm publishing

Usage: 
  python3 mvm.py [flags]

Flags:
  new                           create a new net user
  publish [ADDRESS] [TX HASH]   publish a contract          
        """)

elif argv[1] == "new":
    config = os.popen("%s %s user %s"%(mixincliPATH, botConfigPATH, newNetUsername)).read()

    # Save net user to file
    with open(newNetUserFile, "w") as f:
        f.write(config)
        print("Config saved in %s"%(newNetUserFile))

    # Print UUID in solidity format
    obj = json.loads(config)
    uuid = obj["client_id"]
    pid ="0x" + uuid.replace("-","")
    print("UUID:", uuid)
    print("PID in solidity:",pid)

    # Transfer 10 cnb to net user
    os.popen("%s %s pay %s %s %s -y"%(mixincliPATH, botConfigPATH, uuid, cnbUUID, cnbAMOUNT))

elif argv[1] == "publish":
    # Publish with contract address and TX hash
    if len(argv) <=2:
        print("Format Error. \n\nFORMAT:\n\tpython3 mvm.py publish [ADDRESS] [TX HASH]")
    elif len(argv[2])==42 and len(argv[3])>0:
        os.popen("%s publish -m %s -k %s -a %s -e %s"%(mvmPATH, mvmCONF, newNetUserFile, argv[2], argv[3]))
        with open(newNetUserFile, "r") as f:
            print("MVMProcessId:",json.loads(f.read())["client_id"])
            print("MVMContractAddress:",argv[2])
    else:
        print("Format Error. \n\nFORMAT:\n\tpython3 mvm.py publish [ADDRESS] [TX HASH]")
