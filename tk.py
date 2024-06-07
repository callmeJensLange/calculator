import tkinter as tk
import csv
from tkinter import messagebox

def are_module_entries_filled():
    for key, entry in module_entries.items():
        if entry.get() == "":
            return False
    return True

def convert_comma_to_dot(value):
    return value.replace(',', '.')

def clear_entries(entries):
    for entry in entries.values():
        entry.delete(0, tk.END)

def cal_vmpp_max(pv_module_data):
    anz_module = int(pv_module_data["anz_module"])
    vMPP = float(pv_module_data["vMPP"])
    aVoc = float(pv_module_data["aVoc"])
    tMin = float(pv_module_data["tMin"])
    Vmpp_max = vMPP*(1+(aVoc*(tMin-25)/100))*anz_module
    return Vmpp_max

def cal_vmpp_min(pv_module_data):
    anz_module = int(pv_module_data["anz_module"])
    vMPP = float(pv_module_data["vMPP"])
    aVoc = float(pv_module_data["aVoc"])
    tMax = float(pv_module_data["tMax"])
    Vmpp_min = vMPP*(1+(aVoc*(tMax-25)/100))*anz_module
    return Vmpp_min

def cal_power(pv_module_data):
    anz_module = int(pv_module_data["anz_module"])
    faktor = float(pv_module_data["faktor"])
    pmax = float(pv_module_data["pmax"])
    power = pmax * anz_module * faktor
    return power

def cal_max_leerlaufspannung(pv_module_data):
    voc = float(pv_module_data["voc"])
    aVoc = float(pv_module_data["aVoc"])
    tMin = float(pv_module_data["tMin"])
    anz_module = float(pv_module_data["anz_module"])
    max_leerlaufspannung = voc*(1+(aVoc*(tMin-25)/100))*anz_module
    return max_leerlaufspannung

def cal_impp_max(pv_module_data):
    anz_strings = int(pv_module_data["anz_strings"])
    iMPP = float(pv_module_data["iMPP"])
    alsc = float(pv_module_data["alsc"])
    tMax = float(pv_module_data["tMax"])
    impp_max = iMPP*(1+alsc*(tMax-25)/100)*anz_strings
    return impp_max

def save_dict_to_csv(data_dict, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data_dict.keys())
        writer.writeheader()
        writer.writerow(data_dict)

def save_to_module_dict():
    global ask_questions_pv_modul
    for key, label in module_labels.items():
        value = module_entries[key].get()
        ask_questions_pv_modul[key] = convert_comma_to_dot(value)
    save_dict_to_csv(ask_questions_pv_modul, 'module_data.csv')


def save_to_inverter_dict():
    global ask_questions_wechselrichter
    for key, label in inverter_labels.items():
        value = inverter_entries[key].get()
        ask_questions_wechselrichter[key] = convert_comma_to_dot(value)
    save_dict_to_csv(ask_questions_wechselrichter, 'inverter_data.csv')

def main():
    global ask_questions_pv_modul, ask_questions_wechselrichter, module_labels, module_entries, inverter_labels, inverter_entries, result_entries, module_frame
    global calculate_entries, inverter_data

    root = tk.Tk()
    root.title("PV-Modul Wechselrichter Rechner v0.002")
    root.geometry('800x850')

    ########### PV-Modules Frame ###########
    module_frame = tk.Frame(root, padx=10, pady=10)
    module_frame.grid(row=0, column=0)

    ask_questions_pv_modul = {}  # Dictionary PV-Modules

    module_header_label = tk.Label(module_frame, text="PV-Modules", font=("Helvetica", 16, "bold"))
    module_header_label.grid(row=0, column=0, columnspan=2, pady=10)

    module_questions = {
        "modul_name": "Name des Moduls: ",
        "anz_module": "Anzahl der Module pro String? ",
        "anz_strings": "Anzahl der Strings? ",
        "pmax": "Maximale Leistung in Watt? ",
        "voc": "Leerlaufspannung Voc? ",
        "vMPP": "Spannung im MPP V? ",
        "iMPP": "Strom im MPP A? ",
        "aVoc": "Temp.koeffizient aVoc Prozent/C°? ",
        "alsc": "Temp.koeffizient alsc Prozent/C°? ",
        "tMin": "Temperatur TMIN C°? ",
        "tMax": "Temperatur TMAX C°? ",
        "faktor": "Ertragsfaktor Prozent? "
    }

    module_labels = {}
    module_entries = {}

    for i, (key, question) in enumerate(module_questions.items(), start=1):
        label = tk.Label(module_frame, text=question)
        label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entry = tk.Entry(module_frame)
        entry.grid(row=i, column=1, padx=10, pady=5)
        module_labels[key] = label
        module_entries[key] = entry

    module_save_button = tk.Button(module_frame, text="Save", command=save_to_module_dict)
    module_save_button.grid(row=len(module_questions) + 1, column=0, columnspan=2, pady=10)

    module_clear_button = tk.Button(module_frame, text="Clear", command=lambda: clear_entries(module_entries))
    module_clear_button.grid(row=len(module_questions) + 1, column=1, columnspan=1, pady=10)

    ############## Inverter Frame ###############
    
    inverter_frame = tk.Frame(root, padx=10, pady=10)
    inverter_frame.grid(row=0, column=1, sticky="n")

    ask_questions_wechselrichter = {}  # Dictionary Inverter

    inverter_header_label = tk.Label(inverter_frame, text="Inverter", font=("Helvetica", 16, "bold"))
    inverter_header_label.grid(row=0, column=0, columnspan=2, pady=10)

    inverter_questions = {
        "wr_name": "Namen des Wechselrichters: ",
        "pMax": "Maximale Generatorleistung (PMAX)",
        "vMax": "Maximale Eingangsspannung (VMAX)",
        "vStart": "Start Spannung (VStart)",
        "mpp_min_v": "MPP min Spannung (VMPPMIN)",
        "mpp_max_v": "MPP max Spannung (VMPPMAX)",
        "iMax": "Maximaler Eingangsstrom (IMPPMAX)",
        "kurz_max": "Maximaler Kurzschlussstrom (ISCMAX)"
    }

    inverter_labels = {}
    inverter_entries = {}

    for i, (key, question) in enumerate(inverter_questions.items(), start=1):
        label = tk.Label(inverter_frame, text=question)
        label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entry = tk.Entry(inverter_frame)
        entry.grid(row=i, column=1, padx=10, pady=5)
        inverter_labels[key] = label
        inverter_entries[key] = entry

    inverter_save_button = tk.Button(inverter_frame, text="Save", command=save_to_inverter_dict)
    inverter_save_button.grid(row=len(inverter_questions) + 1, column=0, columnspan=2, pady=10)

    inverter_clear_button = tk.Button(inverter_frame, text="Clear", command=lambda: clear_entries(inverter_entries))
    inverter_clear_button.grid(row=len(inverter_questions) + 1, column=1, columnspan=1, pady=10)

    ############# String Values Frame #############
    
    string_values_frame = tk.Frame(root, padx=10, pady=10)
    string_values_frame.grid(row=1, column=0, sticky="w")

    string_values_header_label = tk.Label(string_values_frame, text="String Values", font=("Helvetica", 16, "bold"))
    string_values_header_label.grid(row=0, column=1, pady=10, sticky="w")

    result_entries = {}

    result_label_1 = tk.Label(string_values_frame, text="Leistung: ")
    result_label_1.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    result_entry_1 = tk.Entry(string_values_frame)
    result_entry_1.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    result_entries["Leistung"] = result_entry_1

    result_label_2 = tk.Label(string_values_frame, text="Max Leerlaufspannung: ")
    result_label_2.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    result_entry_2 = tk.Entry(string_values_frame)
    result_entry_2.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    result_entries["Max Leerlaufspannung"] = result_entry_2

    result_label_3 = tk.Label(string_values_frame, text="Max Spannung im MPP: ")
    result_label_3.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    result_entry_3 = tk.Entry(string_values_frame)
    result_entry_3.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    result_entries["Max Spannung im MPP"] = result_entry_3

    result_label_4 = tk.Label(string_values_frame, text="Min Spannung im MPP: ")
    result_label_4.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    result_entry_4 = tk.Entry(string_values_frame)
    result_entry_4.grid(row=4, column=1, padx=10, pady=5, sticky="w")
    result_entries["Min Spannung im MPP"] = result_entry_4

    result_label_5 = tk.Label(string_values_frame, text="Max Strom im MPP: ")
    result_label_5.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    result_entry_5 = tk.Entry(string_values_frame)
    result_entry_5.grid(row=5, column=1, padx=10, pady=5, sticky="w")
    result_entries["Max Strom im MPP"] = result_entry_5

    ############# Calculate Frame #############
    
    calculate_frame = tk.Frame(root, padx=10, pady=10)
    calculate_frame.grid(row=1, column=1)

    calculate_button = tk.Button(calculate_frame, text="Calculate", command=calculate)
    calculate_button.grid(row=3, column=1, pady=10)

    ############# Entry-Widgets #############

    calculate_entries = {
        "Pmax Status ": tk.Entry(calculate_frame, width=30),
        "Vmax Status ": tk.Entry(calculate_frame, width=30),
        "Vstart Status ": tk.Entry(calculate_frame, width=30),
        "Vmpp Min Status ": tk.Entry(calculate_frame, width=30),
        "Vmpp Max Status ": tk.Entry(calculate_frame, width=30),
        "Impp Max Status ": tk.Entry(calculate_frame, width=30),
        "Isc Max Status ": tk.Entry(calculate_frame, width=30)
    }

    for i, (label_text, entry) in enumerate(calculate_entries.items(), start=4):
        label = tk.Label(calculate_frame, text=label_text)
        label.grid(row=i, column=1, pady=5, sticky="e")
        entry.grid(row=i, column=2, pady=5, padx=5)
        entry.config(state='disabled')

    root.mainloop()

############# Calculate #############
def calculate():
    global inverter_data, result_power, result_max_leerlaufspannung, result_vmpp_min, result_vmpp_max, result_impp_max, result_entries, calculate_entries

    if not are_module_entries_filled():
        messagebox.showerror("Fehler", "Bitte füllen Sie alle Felder im PV-Modul-Abschnitt aus.")
        return

    inverter_data = ask_questions_wechselrichter
    pv_module_data = ask_questions_pv_modul

    result_power = float("{:.2f}".format(cal_power(pv_module_data)))
    result_max_leerlaufspannung = "{:.2f}".format(cal_max_leerlaufspannung(pv_module_data))
    result_vmpp_max = "{:.2f}".format(cal_vmpp_max(pv_module_data))
    result_vmpp_min = "{:.2f}".format(cal_vmpp_min(pv_module_data))
    result_impp_max = "{:.2f}".format(cal_impp_max(pv_module_data))

    result_entries["Max Leerlaufspannung"].delete(0, tk.END)
    result_entries["Max Leerlaufspannung"].insert(0, str(result_max_leerlaufspannung + " V"))

    result_entries["Leistung"].delete(0, tk.END)
    result_entries["Leistung"].insert(0, str(result_power) + " W")

    result_entries["Max Spannung im MPP"].delete(0, tk.END)
    result_entries["Max Spannung im MPP"].insert(0, str(result_vmpp_max + " V"))

    result_entries["Min Spannung im MPP"].delete(0, tk.END)
    result_entries["Min Spannung im MPP"].insert(0, str(result_vmpp_min + " V"))

    result_entries["Max Strom im MPP"].delete(0, tk.END)
    result_entries["Max Strom im MPP"].insert(0, str(result_impp_max + " A"))

    # Ergebnis von check_Pmax in calculate_entry anzeigen
    #print("Inverter Data:", inverter_data)

    pmax_status = check_Pmax(inverter_data, result_power)
    calculate_entries["Pmax Status "].config(state='normal')
    calculate_entries["Pmax Status "].delete(0, tk.END)
    calculate_entries["Pmax Status "].insert(0, pmax_status)
    calculate_entries["Pmax Status "].config(state='disabled')

    # Ergebnis von check_Vmax in calculate_entry anzeigen
    vmax_status = check_Vmax(inverter_data)
    calculate_entries["Vmax Status "].config(state='normal')
    calculate_entries["Vmax Status "].delete(0, tk.END)
    calculate_entries["Vmax Status "].insert(0, vmax_status)
    calculate_entries["Vmax Status "].config(state='disabled')

    # Ergebnisse der anderen Prüfungen anzeigen
    vstart_status = check_V_start(inverter_data)
    calculate_entries["Vstart Status "].config(state='normal')
    calculate_entries["Vstart Status "].delete(0, tk.END)
    calculate_entries["Vstart Status "].insert(0, vstart_status)
    calculate_entries["Vstart Status "].config(state='disabled')

    vmpp_min_status = check_vmpp_min(inverter_data)
    calculate_entries["Vmpp Min Status "].config(state='normal')
    calculate_entries["Vmpp Min Status "].delete(0, tk.END)
    calculate_entries["Vmpp Min Status "].insert(0, vmpp_min_status)
    calculate_entries["Vmpp Min Status "].config(state='disabled')

    vmpp_max_status = check_vmpp_max(inverter_data)
    calculate_entries["Vmpp Max Status "].config(state='normal')
    calculate_entries["Vmpp Max Status "].delete(0, tk.END)
    calculate_entries["Vmpp Max Status "].insert(0, vmpp_max_status)
    calculate_entries["Vmpp Max Status "].config(state='disabled')

    impp_max_status = check_impp_max(inverter_data)
    calculate_entries["Impp Max Status "].config(state='normal')
    calculate_entries["Impp Max Status "].delete(0, tk.END)
    calculate_entries["Impp Max Status "].insert(0, impp_max_status)
    calculate_entries["Impp Max Status "].config(state='disabled')

    isc_max_status = check_isc_max(inverter_data)
    calculate_entries["Isc Max Status "].config(state='normal')
    calculate_entries["Isc Max Status "].delete(0, tk.END)
    calculate_entries["Isc Max Status "].insert(0, isc_max_status)
    calculate_entries["Isc Max Status "].config(state='disabled')

############# Check Inverter #############
def check_Pmax(inverter_data, power):
    pmax = float(inverter_data["pMax"])
    if pmax >= power:
        return "OK"
    else:
        return "Fehler: Pmax überschritten"

def check_Vmax(inverter_data):
    vmax = float(inverter_data["vMax"])
    if vmax > float(result_max_leerlaufspannung):  # vmax
        return "OK"
    else:
        return "Fehler: Vmax überschritten"

def check_V_start(inverter_data):
    vstart = float(inverter_data["vStart"])  # vstart
    if vstart < float(result_vmpp_min):
        return "OK"
    else:
        return "Fehler: Vstart zu niedrig"

def check_vmpp_min(inverter_data):
    vmpp_min = float(inverter_data["mpp_min_v"])  # vmpp_min
    if vmpp_min < float(result_vmpp_min):
        return "OK"
    else:
        return "Fehler: Vmpp Min zu niedrig"

def check_vmpp_max(inverter_data):
    vmpp_max = float(inverter_data["mpp_max_v"])  # vmpp_max
    if vmpp_max > float(result_vmpp_max):
        return "OK"
    else:
        return "Fehler: Vmpp Max überschritten"

def check_impp_max(inverter_data):
    impp_max = float(inverter_data["iMax"])  # impp_max
    if impp_max > float(result_impp_max):
        return "OK"
    else:
        return "Fehler: Impp Max überschritten"

def check_isc_max(inverter_data):
    isc_max = float(inverter_data["kurz_max"])  # isc_max
    if isc_max > float(result_impp_max):
        return "OK"
    else:
        return "Fehler: Isc Max überschritten"

if __name__ == "__main__":
    main()
