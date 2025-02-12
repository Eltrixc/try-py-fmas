import h5py
import numpy as np
import matplotlib.pyplot as plt
from fmas.tools import plot_evolution

# Buka file hasil simulasi
with h5py.File("output/output_file.h5", "r") as f:
    uw = f["uw"][:]  # Medan listrik di domain frekuensi
    z = f["z"][:]
    w = f["w"][:]

# Pastikan tidak ada NaN dalam data
uw = np.nan_to_num(uw)

# Buat plot
plt.figure(figsize=(10, 5))
plt.imshow(np.abs(uw), aspect="auto", extent=[z.min(), z.max(), w.min(), w.max()], cmap="inferno")
plt.colorbar(label="Amplitude")
plt.xlabel("Propagation distance (z)")
plt.ylabel("Frequency (w)")
plt.title("Simulation Result")
plt.savefig("plot_fixed.png")  # Simpan ulang gambar
plt.show()
