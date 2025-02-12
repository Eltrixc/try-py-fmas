import h5py

with h5py.File("input_file.h5", "a") as f:  # Mode "a" = append (tidak hapus data lama)
    f.attrs["t_max"] = 10.0  # Sesuaikan jika perlu

print("Atribut t_max berhasil ditambahkan.")
