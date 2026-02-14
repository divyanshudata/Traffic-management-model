import traci
import time
import os
import sys
import csv

# --- CONFIGURATION ---
SUMO_HOME = r"C:\Users\DIVYANSHU\Sumo"
tools = os.path.join(SUMO_HOME, 'tools')
sys.path.append(tools)
sumoBinary = os.path.join(SUMO_HOME, "bin", "sumo-gui.exe")
sumoCmd = [sumoBinary, "-c", "config.sumocfg"]

def run_god_mode():
    print("🚀 Starting Simulation in GOD MODE (Controlled by Camera)...")
    
    # Reset Data File for Dashboard
    with open("live_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["step", "waiting_cars", "status"])

    traci.start(sumoCmd)
    
    tls_id = None
    tls_list = traci.trafficlight.getIDList()
    if tls_list: tls_id = tls_list[0]
    
    step = 0
    while step < 10000:
        try:
            traci.simulationStep()
        except:
            break
        
        # --- READ FROM CAMERA ---
        camera_count = 0
        try:
            if os.path.exists("sensor_data.txt"):
                with open("sensor_data.txt", "r") as f:
                    data = f.read().strip()
                    if data.isdigit():
                        camera_count = int(data)
        except:
            pass # Ignore read errors (file busy)

        # --- DECISION LOGIC ---
        status = "Normal"
        
        # Trigger if Camera sees more than 5 cars
        if camera_count > 5:
            status = f"CAMERA ALERT: {camera_count} Cars Detected!"
            
            if tls_id:
                try:
                    remaining = traci.trafficlight.getNextSwitch(tls_id) - traci.time.getTime()
                    if remaining < 5:
                        traci.trafficlight.setPhaseDuration(tls_id, remaining + 10)
                        print(f"   >>> 🚦 Light Extended by AI Vision!")
                except:
                    pass

        # --- UPDATE DASHBOARD ---
        if step % 2 == 0:
            try:
                with open("live_data.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([step, camera_count, status])
            except:
                pass

        if step % 10 == 0:
            print(f"Step {step} | 📷 Vision Input: {camera_count} cars | Status: {status}")

        step += 1
        time.sleep(0.1) # Sync speed
        
    try: traci.close()
    except: pass

if __name__ == "__main__":
    run_god_mode()