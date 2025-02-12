import h5py

with h5py.File("input_file.h5", "w") as f:
    f.attrs["t_max"] = 10.0  # Menambahkan atribut yang dibutuhkan
    f.attrs["t_min"] = 0.0   # Bisa ditambahkan jika diperlukan
    f.attrs["dt"] = 0.01     # Parameter lain (sesuaikan jika diperlukan)
    f.create_dataset("example_data", data=[1, 2, 3, 4, 5])

print("File input_file.h5 berhasil dibuat dengan atribut yang diperlukan.")

