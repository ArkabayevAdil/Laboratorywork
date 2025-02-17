import json

print("Interface Status")
print("================================================================================")
print("DN                                                 Description           Speed    MTU")
print("-------------------------------------------------- --------------------  ------  ------")

with open("C:\Users\Asus\Desktop\LaboratoryPP2\LAB4\json\sampledata.json", "r") as f:
    data = json.load(f)

print("Inherit status")
print("="*84)
DN = "DN"
Description = "Description"
Speed = "Speed"
MTU = "MTU"
print(f"{DN:50} {Description:20} {Speed:7} {MTU:10}")
print("-"*84)

for item in data["imdata"]:
    attr = item["l1PhysIf"]["attributes"]
    dn = attr.get("dn", "N/A")
    descr = attr.get("descr", "N/A")
    speed = attr.get("speed", "N/A")
    mtu = attr.get("mtu", "N/A")
    print(f"{dn:50} {descr:20} {speed:7} {mtu:10}")
