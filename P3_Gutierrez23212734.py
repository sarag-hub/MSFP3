"""
Práctica 3: Sistema musculoesqueletico

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Sara Gutierrez Hernandez
Número de control: 23212734
Correo institucional: l23212732@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Librerías
import numpy as np
import control as ctrl
import matplotlib.pyplot as plt

# Parámetros 
F0, alpha, Cs, Cp = 1, 0.25, 10E-6, 100E-6
R_control, R_caso = 100, 10E3

# Sistema musculoesquelético
def musculo(R):
    num = [Cs*R, 1 - alpha]
    den = [R*(Cp + Cs), 1]
    sys = ctrl.tf(num, den)
    polo = -1/(R*(Cp + Cs))
    return sys, polo

# Controlador PI
def controlador(kI,kP,sys):
    Cr = 1E-6
    Re = 1/(Cr*kI)
    Rr = kP*Re
    numPID = [Rr*Cr,1]
    denPID = [Re*Cr,0]
    PID = ctrl.tf(numPID,denPID)
    sysPID = ctrl.feedback(ctrl.series(PID,sys),1,sign=-1)
    return sysPID

# Datos generales 
x0,t0,tend,dt,w,h = 0,0,10,1E-3,10,5
N = round((tend-t0)/dt)+1
t = np.linspace(t0,tend,N)
u = np.zeros(N)
u[round(1/dt):round(2/dt)] = 1           

# Función de transferencia: Control
sysControl, polo = musculo(R_control)
print(f'Función de transferencia del control (R = {R_control} ohm): {sysControl}')
print(f'Polo del sistema: s = {polo:.3f} rad/s (estable)\n')

# Función de transferencia: Caso
sysCaso, polo = musculo(R_caso)
print(f'Función de transferencia del caso (R = {R_caso:.0f} ohm): {sysCaso}')
print(f'Polo del sistema: s = {polo:.3f} rad/s (estable)\n')

# Tratamiento: PI 
kP = 0.0381
kI = 2.3773E4
sysPID = controlador(kP, kI, sysCaso)
print(f'Función de transferencia del caso con PID (lazo cerrado): {sysPID}\n')

# Respuestas
_, Fs_control = ctrl.forced_response(sysControl, t, u, x0)
_, Fs_caso    = ctrl.forced_response(sysCaso, t, u, x0)
_, PID_trat   = ctrl.forced_response(sysPID, t, u, x0)     # referencia: F(t)


plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 11

clr1 = np.array([66, 91, 154])/255
clr2 = np.array([40, 122, 116])/255
clr3 = np.array([151, 40, 40])/255
clr4 = [0.5, 0.5, 0.5]

fg1 = plt.figure(facecolor='w')
plt.plot(t, u,          '-', linewidth=0.25, color=clr1, label=r'$F(t)$')
plt.plot(t, Fs_control, '-', linewidth=0.25, color=clr2, label=r'$Fs(t)$: Control')
plt.plot(t, Fs_caso,    '-', linewidth=0.25, color=clr3, label=r'$Fs(t)$: Caso')
plt.plot(t, PID_trat,   ':', linewidth=0.25, color=clr4, label=r'$PID(t)$: Tratamiento')
plt.grid(False)
yt = np.round(np.arange(-0.1, 1.15, 0.1), 1)
plt.xlim(0, 10);     plt.xticks(np.arange(0, 11, 1))
plt.ylim(-0.1, 1.1); plt.yticks(yt, [f'{v:g}' for v in yt])
plt.tick_params(direction='in', top=True, right=True)
plt.xlabel(r'$t$ [s]')
plt.ylabel(r'$F(t)$ [V]')
plt.legend(bbox_to_anchor=(0.5, 1.02), loc='lower center', ncol=4, frameon=False)
fg1.set_size_inches(w, h)
fg1.tight_layout()
fg1.savefig('Control y caso_python.pdf')
plt.show()