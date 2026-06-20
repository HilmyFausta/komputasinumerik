# PRAKTIKUM KOMNUM 6 KELOMPOK 7 (Analisis Perbandingan Metode Trapezoidal dan Romberg)

|    NRP     |           Nama             |
| :--------: |       :------------:       |
| 5025251046 | Muhammad Fairuz Ananta       |
| 5025251028 | Julianda Caesar Prakoso      |
| 5025251052 | Hilmy Fausta Pratama|


## Rumus Fundamental

### 1. Aturan Trapezoidal

Konsep dasar dari trapezoidal adalah membagi area integral total menjadi sub-interval yang berjarak sama (equispaced), di mana lebar setiap pias dinotasikan sebagai $\Delta x$ (atau $h$).

$$I = \frac{\Delta x}{2} \left[ f(x_0) + 2 \sum_{i=1}^{n-1} f(x_i) + f(x_n) \right]$$

### 2. Metode Integrasi Romberg

Metode Romberg memanfaatkan hasil dari metode Trapezoidal pada kolom pertama ($R_{i,0}$) dengan jumlah pias yang terus dilipatgandakan ($n = 1, 2, 4, 8, \dots$). Demgan Ekstrapolasi Richardson, Metode Romberg bisa mengeliminasi suku galat/error tanpa perlu menghitung turunan fungsi secara manual.

Ruumus pengisian matriks segitiga bawah Romberg adalah:

$$R_{i,j} = R_{i,j-1} + \frac{R_{i,j-1} - R_{i-1,j-1}}{4^j - 1}$$

Dimana:
* $R_{i,0}$: Hasil aturan Trapezoidal komposit pada baris ke-$i$ dengan jumlah interval $n = 2^i$.
* $i$: Indeks baris/kerapatan pias ($i \ge 0$).
* $j$: Indeks kolom/orde akurasi ekstrapolasi ($j \ge 1$).
---

## Penjelasan Kode
1. Menyediakan library eksternal, numpy untuk komputasi saintifik, matplotlib untuk visualisasi data grafik, scipy.integrate untuk menghitung nilai eksak integral
```py
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
```

2. Memasukan fungsi target yang akan dicari, batas atas dan bawah, serta max orde sebagai Konstanta penentu dimensi matriks persegi Romberg ($n \times n$). Ini juga mengontrol batas atas iterasi. Karena jumlah pias ($n$) bersifat eksponensial ($2^{\text{orde}}$), misal nilai 6 berarti kita akan menguji pias dari $2^0 = 1$ hingga maksimum $2^5 = 32$ pias.
```py
# edit fungsi dan batas
def f(x):
    return np.exp(x) * np.sin(x)

a = 0.0
b = 3.0
max_orde = 6
```

3. Meenghitung metode trapezoidal
```py
def trapezoidal(f, a, b, n):
    h = (b - a) / n
    total = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        total += f(a + i * h)
    return total * h
```

4. Menghitung dengan metode romberg
```py
def romberg(f, a, b, max_ord):
    R = np.zeros((max_ord, max_ord))
    
    for i in range(max_ord):
        n = 2**i
        R[i, 0] = trapezoidal(f, a, b, n)
        
    for j in range(1, max_ord):
        for i in range(j, max_ord):
            R[i, j] = R[i, j-1] + (R[i, j-1] - R[i-1, j-1]) / ((4**j) - 1)
            
    return R
```

5. Menghitung nilai asli integral fungsi, dan memanggil fungsi romberg disimpan di tabel R
```py
nilai_eksak, _ = quad(f, a, b)
tabel_R = romberg(f, a, b, max_orde)
```

6. Menghitung error untuk kedua metode, n untuk jumlah pias tiap orde 1, 2, 4, 8, 16,...
```py
error_trapezoidal = [abs(tabel_R[i, 0] - nilai_eksak) for i in range(max_orde)]
error_romberg = [abs(tabel_R[i, i] - nilai_eksak) for i in range(max_orde)]
n_evaluasi = [2**i for i in range(max_orde)]
```

7. Menampilkan nilai eksak dengan ketelitian 10 angka dibelakang koma
```py
print("="*80)
print(f"Hasil Integral Eksak : {nilai_eksak:.10f}")
print("="*80)
```

8. Menampilkan tabel hasil metode trapezoida
```py
print("\nTABEL HASIL TRAPEZOIDAL")
print("-" * 40)
print(f"{'Orde':<5} | {'n':<4} | {'Hasil Trapezoidal'}")
print("-" * 40)
for i in range(max_orde):
    print(f"{i:<5} | {n_evaluasi[i]:<4} | {tabel_R[i,0]:.10f}")
```

9. Menampilkan segitiga bawah untuk metode romberg dengan nested loop
```py
#tabel matriks romberg
print("\nTABEL MATRIKS ROMBERG")
print("Dengan Ekstrapolasi Richardson")
print("-" * 90)
for i in range(max_orde):
    baris = f"Orde {i} (n = {n_evaluasi[i]:2}): "
    for j in range(max_orde):
        if j <= i:
            baris += f"{tabel_R[i,j]:14.10f} "
    print(baris)
```

10. Melakukan perbandingan untuk nilai error metode trapezoidal dan metode romberg yang disandingkan
```py
print("\nTABEL PERBANDINGAN ERROR PER ORDE")
print("-" * 65)
print(f"{'Orde':<5} | {'n':<4} | {'Error Trapezoidal':<20} | {'Error Romberg'}")
print("-" * 65)
for i in range(max_orde):
    print(f"{i:<5} | {n_evaluasi[i]:<4} | {error_trapezoidal[i]:<20.10f} | {error_romberg[i]:.10f}")
print("-" * 65)
```

11. Menampilkan visualisasi grafik perbandingan error
```py
plt.figure(figsize=(8, 5))
plt.plot(n_evaluasi, error_trapezoidal, marker='o', linestyle='-', label='Error Trapezoidal', color='red')
plt.plot(n_evaluasi, error_romberg, marker='s', linestyle='-', label='Error Romberg', color='blue')

plt.yscale('log')
plt.xlabel('Jumlah Pias / Interval (n)')
plt.ylabel('Galat Absolut (Log Scale)')
plt.title('Perbandingan Penurunan Galat: Trapezoidal vs Romberg')
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()
```

## Screenshot Cara Kerja
hasil ketika di run
<img width="900" height="724" alt="image" src="https://github.com/user-attachments/assets/ffe2130c-4fe7-474e-b0cc-227d00694c41" />


hasil grafik perbedaan
<img width="920" height="622" alt="image" src="https://github.com/user-attachments/assets/4ea032cb-857c-4001-bd78-d85114c105e5" />

## Kesimpulan
Perbandingan kedua metode ini terletak pada cara keduanya memangkas error untuk mencapai nilai eksak. Metode Trapezoidal menggunakan pendekatan tradisional dengan meningkatkan jumlah pias (n) secara terus menerus agar semakin rapat. Namun, pada kurva yang ekstrem, metode ini membutuhkan pias yang sangat besar sehingga komputasi menjadi lambat dan kurang efisien. Sebaliknya, Integrasi Romberg menggunakan pendekatan yang lebih cerdas melalui Ekstrapolasi Richardson. Romberg memanfaatkan pola error dari hasil Trapezoidal dasar dan mengeliminasinya secara sistematis lewat operasi aljabar. menjadikannya algoritma yang jauh lebih efisien, hemat daya komputasi, dan lebih efektif dibandingkan Trapezoidal Tradisional


## Kode Full
```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# edit fungsi dan batas
def f(x):
    return np.exp(x) * np.sin(x)

a = 0.0
b = 3.0
max_orde = 6 

#metode trapezoidal
def trapezoidal(f, a, b, n):
    h = (b - a) / n
    total = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        total += f(a + i * h)
    return total * h

#metode romberg
def romberg(f, a, b, max_ord):
    R = np.zeros((max_ord, max_ord))
    
    for i in range(max_ord):
        n = 2**i
        R[i, 0] = trapezoidal(f, a, b, n)
        
    for j in range(1, max_ord):
        for i in range(j, max_ord):
            R[i, j] = R[i, j-1] + (R[i, j-1] - R[i-1, j-1]) / ((4**j) - 1)
            
    return R

#nilai asli integral fungsi
nilai_eksak, _ = quad(f, a, b)
tabel_R = romberg(f, a, b, max_orde)

#menghitung error
error_trapezoidal = [abs(tabel_R[i, 0] - nilai_eksak) for i in range(max_orde)]
error_romberg = [abs(tabel_R[i, i] - nilai_eksak) for i in range(max_orde)]
n_evaluasi = [2**i for i in range(max_orde)]

#print
print("="*80)
print(f"Hasil Integral Eksak : {nilai_eksak:.10f}")
print("="*80)

#tabel trapezoidal
print("\nTABEL HASIL TRAPEZOIDAL")
print("-" * 40)
print(f"{'Orde':<5} | {'n':<4} | {'Hasil Trapezoidal'}")
print("-" * 40)
for i in range(max_orde):
    print(f"{i:<5} | {n_evaluasi[i]:<4} | {tabel_R[i,0]:.10f}")

#tabel matriks romberg
print("\nTABEL MATRIKS ROMBERG")
print("Dengan Ekstrapolasi Richardson")
print("-" * 90)
for i in range(max_orde):
    baris = f"Orde {i} (n = {n_evaluasi[i]:2}): "
    for j in range(max_orde):
        if j <= i:
            baris += f"{tabel_R[i,j]:14.10f} "
    print(baris)

#tabel error
print("\nTABEL PERBANDINGAN ERROR PER ORDE")
print("-" * 65)
print(f"{'Orde':<5} | {'n':<4} | {'Error Trapezoidal':<20} | {'Error Romberg'}")
print("-" * 65)
for i in range(max_orde):
    print(f"{i:<5} | {n_evaluasi[i]:<4} | {error_trapezoidal[i]:<20.10f} | {error_romberg[i]:.10f}")
print("-" * 65)


#grafik
plt.figure(figsize=(8, 5))
plt.plot(n_evaluasi, error_trapezoidal, marker='o', linestyle='-', label='Error Trapezoidal', color='red')
plt.plot(n_evaluasi, error_romberg, marker='s', linestyle='-', label='Error Romberg', color='blue')

plt.yscale('log')
plt.xlabel('Jumlah Pias / Interval (n)')
plt.ylabel('Galat Absolut (Log Scale)')
plt.title('Perbandingan Penurunan Galat: Trapezoidal vs Romberg')
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()
```
