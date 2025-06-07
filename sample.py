import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk


def input_voltage(t, type='step', amp=10, freq=1, duration=1):
    if type == 'step':
        return amp if t < duration else 0
    elif type == 'triangle':
        return amp * (1 - 2 * abs((t % (1 / freq)) * freq - 0.5))
    elif type == 'sin':
        return amp * np.sin(2 * np.pi * freq * t)
    return 0


def simulate_motor(R=1, L=0.5, K_T=0.1, K_e=0.1, J=0.01, B=0.02, input_type='step', amp=10, freq=1, duration=1, t_max=5,
                   dt=0.001):
    t_values = np.arange(0, t_max, dt)
    i_values = np.zeros_like(t_values)
    v_values = np.zeros_like(t_values)
    omega_values = np.zeros_like(t_values)

    i = 0
    omega = 0

    for n in range(1, len(t_values)):
        t = t_values[n]
        V = input_voltage(t, input_type, amp, freq, duration)

        di_dt = (V - R * i - K_e * omega) / L
        domega_dt = (K_T * i - B * omega) / J

        i += di_dt * dt
        omega += domega_dt * dt

        v_values[n] = V
        i_values[n] = i
        omega_values[n] = omega

    # Wykresy wyników

    plt.figure(figsize=(10, 5))
    plt.subplot(3, 1, 1)
    plt.plot(t_values, v_values, label='Sygnał zadany u(t) (V)')
    plt.legend()
    plt.grid()

    plt.subplot(3, 1, 2)
    plt.plot(t_values, i_values, label='Prąd (A)')
    plt.legend()
    plt.grid()

    plt.subplot(3, 1, 3)
    plt.plot(t_values, omega_values, label='Prędkość kątowa (rad/s)', color='r')
    plt.legend()
    plt.grid()

    plt.show()


def start_simulation():
    try:
        simulate_motor(
            input_type=signal_var.get(),
            amp=float(sliders['Amplitude'].get()),
            freq=float(sliders['Frequency'].get()),
            duration=float(sliders['Duration'].get()),
            t_max=float(sliders['t_max'].get()),
            R=float(entries['R'].get()),
            L=float(entries['L'].get()),
            K_T=float(entries['K_T'].get()),
            K_e=float(entries['K_e'].get()),
            J=float(entries['J'].get()),
            B=float(entries['B'].get()),
            dt=float(entries['dt'].get())
        )
    except ValueError:
        print("Niepoprawnie wypełnione pole.")


root = tk.Tk()
root.title("options")
root.geometry("450x750")
root.configure(bg='#f0f0c0')

signal_var = tk.StringVar(value='step')

signal_frame = tk.LabelFrame(root, text="Signal Type", bg='#f5d764', font=('Arial', 12, 'bold'), padx=10, pady=10)
signal_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

for i, label in enumerate(['step', 'triangle', 'sin']):
    tk.Radiobutton(signal_frame, text=label, variable=signal_var, value=label,
                   font=('Arial', 10), bg='#b1ebfa', width=20, anchor='w').grid(row=i, column=0, sticky='w', pady=2)

slider_frame = tk.LabelFrame(root, text="Signal Parameters", bg='#f5d764', font=('Arial', 12, 'bold'), padx=10, pady=10)
slider_frame.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

param1 = {
    'Amplitude': (0.1, 20, 0.1, 2),
    'Frequency': (0.1, 10, 0.1, 1),
    'Duration': (0, 20, 0.1, 5),
    't_max': (1, 30, 0.1, 7),
}

sliders = {}
for i, (label, (min_val, max_val, step, default)) in enumerate(param1.items()):
    tk.Label(slider_frame, text=label, font=('Arial', 10), bg='#b1ebfa', width=15, anchor='w').grid(row=i, column=0,
                                                                                                    sticky='w', pady=2)
    scale = tk.Scale(slider_frame, from_=min_val, to=max_val, resolution=step, orient='horizontal', length=250,
                     bg='#b1ebfa')
    scale.set(default)
    scale.grid(row=i, column=1, pady=2)
    sliders[label] = scale

entry_frame = tk.LabelFrame(root, text="Motor Parameters", bg='#f5d764', font=('Arial', 12, 'bold'), padx=10, pady=10)
entry_frame.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

param2 = ['R', 'L', 'K_T', 'K_e', 'J', 'B', 'dt']
default_values = {
    'R': 1, 'L': 0.5, 'K_T': 0.1, 'K_e': 0.1, 'J': 0.01, 'B': 0.02, 'dt': 0.001
}
entries = {}
for i, label in enumerate(param2):
    tk.Label(entry_frame, text=label, font=('Arial', 10), bg='#b1ebfa', width=10, anchor='w').grid(row=i, column=0,
                                                                                                   sticky='w', pady=2)
    entry = tk.Entry(entry_frame)
    entry.insert(0, str(default_values[label]))
    entry.grid(row=i, column=1, pady=2)
    entries[label] = entry

button = tk.Button(root, text="Simulate", command=start_simulation, font=('Arial', 12, 'bold'), bg='#a4ddaa')
button.grid(row=3, column=0, pady=20)

root.mainloop()