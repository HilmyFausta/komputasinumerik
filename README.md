# Integrasi Numerik: Analisis Perbandingan Metode Trapezoidal dan Romberg

Repository ini berisi implementasi mandiri untuk menghitung integral tentu menggunakan **Metode Trapezoidal** dan **Integrasi Romberg (Ekstrapolasi Richardson)**. Kode ini dirancang untuk membandingkan performa akurasi (galat/error) serta efisiensi konvergensi dari kedua metode tersebut secara objektif.

## 📌 Rumus Fundamental

### 1. Aturan Trapezoidal (Komposit)
Metode ini mendekati area di bawah kurva dengan membaginya menjadi beberapa pias berbentuk trapesium.
$$\int_{a}^{b} f(x) \,dx \approx \frac{h}{2} \left[ f(a) + 2\sum_{i=1}^{n-1} f(a+ih) + f(b) \right]$$

### 2. Ekstrapolasi Richardson (Integrasi Romberg)
Romberg memperbaiki hasil Trapezoidal kolom pertama ($R_{i,0}$) menggunakan kombinasi linear dari dua taksiran berurutan untuk mengeliminasi suku galat dominan.
$$R_{i,j} = R_{i,j-1} + \frac{R_{i,j-1} - R_{i-1,j-1}}{4^j - 1}$$

---

## 🛠️ Analisis Struktur Kode & Per Fungsi

Kode program dipecah menjadi beberapa fungsi modular berdasarkan tanggung jawab logikanya masing-masing.

### 1. Definisi Matematis Fungsi Target (`f`)
Fungsi ini bertindak sebagai *Mathematical Engine Core* yang mendefinisikan persamaan integral yang akan diselesaikan.

```python
def f(x):
    return np.exp(x) * np.sin(x)