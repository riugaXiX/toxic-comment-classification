import pandas as pd

# Baca data dari file CSV
# Ganti 'path_to_your_file.csv' dengan path file Anda
df = pd.read_csv('data/preprocessing.csv')

# Daftar label yang ada dalam dataset
labels = ['pornografi', 'sara', 'radikalisme', 'pencemaran_nama_baik']

# Mengonversi kolom label menjadi tipe data numerik (jika belum)
for label in labels:
    df[label] = pd.to_numeric(df[label], errors='coerce').fillna(0).astype(int)

# Menampilkan distribusi label sebelum pemilihan sampel
print("Distribusi Label Sebelum Pemilihan Sampel:")
print(df[labels].sum())

# Menyimpan sampel yang dipilih
selected_samples = pd.DataFrame()

# Mengambil 50 sampel untuk setiap label
for label in labels:
    # Filter data yang sesuai dengan label
    filtered_data = df[df[label] == 1]
    
    # Jika jumlah data yang difilter kurang dari 50, ambil semua data
    if len(filtered_data) < 50:
        selected_samples = pd.concat([selected_samples, filtered_data])
    else:
        selected_samples = pd.concat([selected_samples, filtered_data.sample(50)])

# Menyimpan data terpilih ke file baru
selected_samples.to_csv('selected_samples.csv', index=False)

# Menampilkan distribusi label setelah pemilihan sampel
print("\nDistribusi Label Setelah Pemilihan Sampel:")

print(selected_samples[labels].sum())
print(df.shape)