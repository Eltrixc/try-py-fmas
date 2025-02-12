import h5py
import numpy as np
import matplotlib.pyplot as plt

# Ganti dengan nama file hasil simulasi
output_file = "output_file.h5"

# Buka file hasil simulasi
with h5py.File(output_file, "r") as f:
    # Cek daftar dataset yang tersedia
    print("Dataset dalam file:", list(f.keys()))

    # Ambil data grid waktu dan hasil simulasi
    t = f["t"][:]
    z = f["z"][:]
    u_z = f["u"][:]  # Asumsi ini pulsa dalam domain waktu

# Plot hasilnya
plt.figure(figsize=(8, 6))
plt.imshow(np.abs(u_z)**2, extent=[z.min(), z.max(), t.min(), t.max()], aspect="auto", origin="lower")
plt.xlabel("Propagation Distance (z)")
plt.ylabel("Time (t)")
plt.title("Pulse Evolution")
plt.colorbar(label="Intensity")
plt.show()
