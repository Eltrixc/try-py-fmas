import os
import numpy as np
import h5py
import sys
from fmas.models import FMAS_S_R
from fmas.solver import IFM_RK4IP
from fmas.data_io import save_h5, read_h5 
from fmas.tools import plot_evolution

# Definisikan fungsi beta_fun_detuning(w)
def beta_fun_detuning(w):
    """Function defining propagation constant."""
    b2 = -1.1830e-2     # (fs^2/micron)
    b3 = 8.1038e-2      # (fs^3/micron)
    b4 = -0.95205e-1    # (fs^4/micron)
    b5 = 2.0737e-1      # (fs^5/micron)
    b6 = -5.3943e-1     # (fs^6/micron)
    b7 = 1.3486         # (fs^7/micron)
    b8 = -2.5495        # (fs^8/micron)
    b9 = 3.0524         # (fs^9/micron)
    b10 = -1.7140       # (fs^10/micron)

    beta_fun = np.poly1d([b10/3628800, b9/362880, b8/40320, b7/5040, b6/720,
                          b5/120, b4/24, b3/6, b2/2, 0., 0.])
    return beta_fun(w)

# Nama file input & output
input_file = "input_file.h5"
output_file = "output/output_file.h5"

# Pastikan folder output ada
os.makedirs("output", exist_ok=True)

# Load parameter dari file input
with h5py.File(input_file, "r") as f:
    par_dict = {key: f[key][()] for key in f.keys()}

# -- COMPUTATIONAL DOMAIN
t_max = 2000.       # (fs)
t_num = 2**14       # (-)
z_max = 50000     # (micron)
z_num = 102       # (-)
z_skip = 20         # (-)

# Buat grid waktu
t = np.linspace(-t_max, t_max, t_num, endpoint=False)

# Buat grid frekuensi
w = np.fft.fftfreq(t.size, d=t[1] - t[0]) * 2 * np.pi

# ... MODEL SPECIFIC PARAMETERS
# ... PROPAGATION CONSTANT
c = 0.29979         # (fs/micron)
lam0 = 0.835        # (micron)
w0 = 2*np.pi*c/lam0 # (rad/fs)

beta_w = beta_fun_detuning(w - w0)  # Sesuaikan detuning
gam0 = 0.11e-6      # (1/W/micron)
n2 = gam0 * c / w0  # (micron^2/W)

# ... PARAMETERS FOR RAMAN RESPONSE
fR = 0.18           # (-)
tau1 = 12.2         # (fs)
tau2 = 32.0         # (fs)

# ... INITIAL CONDITION
t0 = 28.4           # (fs)
P0 = 1e4            # (W)
E_0t_fun = lambda t: np.real(np.sqrt(P0)/np.cosh(t/t0) * np.exp(-1j * w0 * t))
E_0t = E_0t_fun(t)

default_params = {
    "t_num": t_num,
    "t_max": t_max, 
    "z_max": 50000,  
    "z_num": 102,
    "beta_w": beta_w,  
    "n2": 1e-20,
    "fR": 0.18,
    "tau1": 12.2e-3,
}

# Memuat parameter dari file input (jika ada)
if os.path.exists(input_file):
    with h5py.File(input_file, "r") as f:
        par_dict = {key: f[key][()] for key in f.keys()}
else:
    par_dict = {}

# Pastikan `z_max` dan `z_num` ada di `par_dict`
for key, val in default_params.items():
    par_dict.setdefault(key, val)

# Pastikan `z_max` dan `z_num` masuk dalam filtered_par_dict
filtered_par_dict = {
    "beta_w": par_dict["beta_w"],
    "n2": par_dict["n2"],
    "fR": par_dict["fR"],
    "tau1": par_dict["tau1"],
    "w": w,
    "z_max": par_dict["z_max"],
    "z_num": par_dict["z_num"],
}


filtered_par_dict = {
    "beta_w": beta_w,  # Sudah dihitung di atas
    "n2": n2,
    "fR": fR,
    "tau1": tau1,
    "w": w, 
}

# Buat model
model = FMAS_S_R(**filtered_par_dict)
solver = IFM_RK4IP(model.Lw, model.Nw)

# Terapkan kondisi awal
solver.set_initial_condition(model.w, np.nan_to_num(model.hRw))

# Jalankan simulasi
print("🚀 Menjalankan simulasi...")
print("✅ Model berhasil dibuat:", model)
print("🔍 Atribut model:", dir(model))
solver.set_initial_condition(model.w, model.hRw)
solver.propagate(z_range=par_dict["z_max"], n_steps=par_dict["z_num"], n_skip=1)

save_h5(output_file, w=model.w, z=solver.z, uw=solver.uwz)

print(f"📂 Hasil simulasi disimpan di '{output_file}' ✅")
print("🎉 Simulasi berhasil!")
