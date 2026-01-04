from pymodbus.client import ModbusTcpClient
import time
import math
import random
import matplotlib.pyplot as plt

PLC_IP = '192.168.1.102'

MASS = 300.0       # kg (Corner of a car)
K_SPRING = 20000.0 # Spring Stiffness
DT = 0.05          # Time speed (50ms)

try:
    client = ModbusTcpClient(PLC_IP, port=502)
    client.connect()
    print("✅ PLC Connected!")
except:
    print("❌ PLC Failed. Is it running?")
    exit()

plt.ion()
fig, ax = plt.subplots()
plt.title("Active Suspension: Road vs. Car")
plt.ylim(0, 100)
line_road, = ax.plot([], [], 'g-', label='Road (Bumps)')
line_car, = ax.plot([], [], 'b-', label='Car Body', linewidth=3)
plt.legend(loc='upper right')

data_road = [50]*100
data_car = [50]*100

car_height = 50.0  # Start in the middle
road_height = 50.0
velocity = 0.0
time_step = 0

print("🏎️ Running! Press Ctrl+C to Stop.")

try:
    while True:
        # A. MAKE THE ROAD BUMPY
        # Sine wave (hills) + Random noise (rocks)
        road_height = 50 + (15 * math.sin(time_step * 0.5)) + random.randint(-2, 2)

        # B. READ "ACTIVE FORCE" FROM PLC (The Actuator)
        # The PLC tells us: "Push Up" or "Pull Down"
        res = client.read_input_registers(0, count=1) # Reading Register 0
        plc_force_command = 50 # Default is "Do nothing"
        if not res.isError():
            plc_force_command = res.registers[0]
        
        # Convert PLC (0-100) to Force
        # 50 = No Force. >50 = Push Up. <50 = Pull Down.
        active_force = (plc_force_command - 50) * 100 

        # C. PHYSICS ENGINE (Simple Version)
        # 1. Spring Force: If Road is higher than Car, Spring pushes Car UP.
        spring_force = (road_height - car_height) * 10
        
        # 2. Total Push on Car = Spring + Active Actuator
        total_force = spring_force + active_force

        # 3. Move the Car (Newton's Law: Force -> Acceleration -> Move)
        velocity = velocity + (total_force / MASS)
        car_height = car_height + velocity

        # Friction/Gravity (Keeps it realistic)
        velocity = velocity * 0.9 # Air resistance
        
        # D. SEND CAR HEIGHT TO PLC (The Sensor)
        # The PLC needs to know where the car is to fix it.
        send_val = int(car_height)
        if send_val < 0: send_val = 0
        if send_val > 100: send_val = 100
        client.write_register(0, send_val) # Writing to Register 0
        # --- NEW DEBUGGING PRINT ---
        # This tells us exactly why the car is invisible
        print(f"Road: {road_height:.1f} | Car: {car_height:.1f} | PLC sends: {plc_force_command}")

        # E. DRAW GRAPH
        data_road.append(road_height)
        data_car.append(car_height)
        data_road.pop(0)
        data_car.pop(0)
        
        line_road.set_ydata(data_road)
        line_road.set_xdata(range(len(data_road)))
        line_car.set_ydata(data_car)
        line_car.set_xdata(range(len(data_car)))
        plt.pause(0.01)
        
        time_step += 0.2

except KeyboardInterrupt:
    print("Stopped.")
    client.close()