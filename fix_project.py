import os
import sys
import subprocess

# --- CONFIGURATION ---
SUMO_HOME = r"C:\Users\DIVYANSHU\Sumo"
PROJECT_DIR = r"C:\Users\DIVYANSHU\Desktop\SIH_Project"

if os.path.exists(SUMO_HOME):
    sys.path.append(os.path.join(SUMO_HOME, 'tools'))
import sumolib

os.chdir(PROJECT_DIR)
print(f"🔧 Fixing project in: {PROJECT_DIR}")

# --- 1. DELETE OLD MAP ---
net_file = "intersection.net.xml"
if os.path.exists(net_file):
    try:
        os.remove(net_file)
        print("🗑️  Old map deleted.")
    except PermissionError:
        print("⚠️  ERROR: Please CLOSE the SUMO window completely first!")
        sys.exit()

# --- 2. RE-GENERATE MAP (FORCE TRAFFIC LIGHTS) ---
print("🗺️  Generating new map with Traffic Lights...")
netgenerate_exe = os.path.join(SUMO_HOME, "bin", "netgenerate.exe")

subprocess.run([
    netgenerate_exe, 
    "--spider", 
    "--spider.arm-number=4", 
    "--output-file=" + net_file, 
    "--no-turnarounds",
    "--default-junction-type", "traffic_light",  # <--- CRITICAL FIX
    "--tls.guess"                                # <--- CRITICAL FIX
], check=True)

# --- 3. AUTO-DETECT CORRECT ROAD NAMES ---
print("🕵️  Detecting road names...")
try:
    net = sumolib.net.readNet(net_file)
except Exception as e:
    print(f"❌ Error reading net: {e}")
    sys.exit()

all_edges = [e.getID() for e in net.getEdges()]
incoming = [e for e in all_edges if not e.startswith(":") and "to" in e]
if not incoming: incoming = [e for e in all_edges if not e.startswith(":")]

if len(incoming) < 2:
    print("❌ Error: Not enough roads found.")
    sys.exit()

route_start = incoming[0] 
route_end = incoming[-1]
print(f"✅ Route: From '{route_start}' to '{route_end}'")

# --- 4. WRITE TRAFFIC FILE ---
traffic_xml = f"""<routes>
    <vType id="car" accel="0.8" decel="4.5" length="5.0" maxSpeed="70.0"/>
    <flow id="flow1" type="car" begin="0" end="2000" number="100" from="{route_start}" to="{route_end}"/>
</routes>
"""

with open("traffic.rou.xml", "w") as f:
    f.write(traffic_xml)
    print("🚗 Traffic file fixed.")

print("\n🎉 REPAIR COMPLETE. Now run 'python main.py'!")