import h5py

with h5py.File("input_file.h5", "a") as f:  # Mode "a" untuk edit tanpa hapus isi lama
    f.attrs["t_max"] = float(f.attrs["t_max"])  # Konversi ke float biasa
    f.attrs["t_min"] = float(f.attrs["t_min"])
    f.attrs["dt"] = float(f.attrs["dt"])

print("File input_file.h5 berhasil diperbaiki.")

