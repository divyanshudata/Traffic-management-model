import os
import subprocess
import sys

# --- 1. CONFIGURATION ---
SUMO_HOME = r"C:\Users\DIVYANSHU\Sumo"
PROJECT_DIR = r"C:\Users\DIVYANSHU\Desktop\SIH_Project"

if not os.path.exists(PROJECT_DIR):
    os.makedirs(PROJECT_DIR)
os.chdir(PROJECT_DIR)

print(f"Working in: {PROJECT_DIR}")

# --- 2. GENERATE MAP ---
netgenerate_exe = os.path.join(SUMO_HOME, "bin", "netgenerate.exe")
try:
    subprocess.run([netgenerate_exe, "--spider", "--spider.arm-number=4", "--output-file=intersection.net.xml", "--no-turnarounds"], check=True)
    print("Map created.")
except:
    print("Could not create map (might already exist). continuing...")

# --- 3. CREATE TRAFFIC FILE ---
traffic_xml = """<routes>
    <vType id="car" accel="0.8" decel="4.5" length="5.0" maxSpeed="70.0"/>
    <flow id="NS" type="car" begin="0" end="1000" number="100" from="2to0" to="0to4"/>
    <flow id="EW" type="car" begin="0" end="1000" number="100" from="3to0" to="0to1"/>
</routes>"""

with open("traffic.rou.xml", "w") as f:
    f.write(traffic_xml)

# --- 4. CREATE CONFIG FILE ---
config_xml = """<configuration>
    <input>
        <net-file value="intersection.net.xml"/>
        <route-files value="traffic.rou.xml"/>
    </input>
    <time>
        <begin value="0"/>
        <end value="2000"/>
    </time>
</configuration>"""

with open("config.sumocfg", "w") as f:
    f.write(config_xml)

# --- 5. CREATE MAIN PYTHON CONTROLLER ---
# We use a raw string (r) to avoid any escape character issues
main_py_code = r"""import traci
import time
import os
import sys

# POINT TO YOUR SUMO FOLDER
SUMO_HOME = r"C:\Users\DIVYANSHU\Sumo"

if os.path.exists(SUMO_HOME):
    tools = os.path.join(SUMO_HOME, 'tools')
    sys.path.append(tools)
else:
    sys.exit(f"Error: Could not find SUMO at {SUMO_HOME}")

sumoBinary = os.path.join(SUMO_HOME, "bin", "sumo-gui.exe")
sumoCmd = [sumoBinary, "-c", "config.sumocfg"]

def run():
    print("Launching SUMO...")
    traci.start(sumoCmd)
    
    step = 0
    while step < 1000:
        traci.simulationStep()
        step += 1
        time.sleep(0.05)
        
    traci.close()

if __name__ == "__main__":
    run()
"""

with open("main.py", "w") as f:
    f.write(main_py_code)

print("SUCCESS! All files created.")