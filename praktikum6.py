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