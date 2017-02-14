# Selamat Datang di Repository Quant.id

# Misi

Ini merupakan proyek non-profit yang bertujuan untuk saling sharing
strategi antar kita sesama ritel untuk meningkatkan pengetahuan,
kemampuan, dan pada akhirnya cuan kita bersama. 

Silakan Anda pakai semua yang ada di sini baik untuk kepentingan
personal maupun professional. Anda mendapatkan keuntungan trading
karena menggunakan strategi di sini, saya ikut senang. Tapi please
strategi atau chart dari sini jangan dijual ulang atau diikutkan 
dalam paket yang dijual, karena itu sangat tidak etis. 

Repository ini berlisensi Open Source yaitu GPL (GNU General Public 
License) versi 2 atau lebih baru. Artinya, kurang lebih, kalau Anda 
memodifikasi file-file dari sini, baik itu chart, AFL, dokumentasi, 
dsb, Anda diharapkan men-share kembali hasil modifikasi Anda kepada
masyarakat secara free juga. Kalau semua men-share hasil penemuannya,
diharapkan tujuan proyek ini untuk meningkatkan pengetahuan, kemampuan,
dan cuan kita bersama bisa tercapai.


# Langkah-langkah Penyetelan

## Download Repository

Langkah pertama adalah men-download isi repository ini ke direktori
AmiBroker di komputer Anda. Direktori AmiBroker Anda bisa di 
`C:\Program Files\AmiBroker` atau `C:\Program Files (x86)\AmiBroker`
tergantung jenis komputer Anda dan versi mana yang terinstall (32bit
atau 64bit). 

Untuk tutorial ini saya asumsikan AmiBroker Anda terinstall di
`C:\Program Files\AmiBroker`. Kalau Amibroker terinstall di tempat
lain, silakan disesuaikan petunjuk di sini dengan lokasi AmiBroker Anda. 

Ada dua cara untuk mendownload repository quant.id.

**Cara 1: dengan memakai program Git**

Cara ini lebih diutamakan karena Anda bisa berkolaborasi untuk memodifikasi
file-file di repository ini. Tapi cara ini lebih sulit dan biasanya hanya 
programmer/software developer yang tahu. Kalau Anda sudah tahu, silakan 
_clone_ repository ini ke direktori AmiBroker, misalnya:

```
cd "Program Files\AmiBroker"

git clone https://github.com/bennylp/quant.id.git 
```

**Cara 2: download ZIP** 

Kalau Anda tidak punya program Git di komputer, Anda bisa download ZIP
dari tombol **"Clone or download"** yang berwarna hijau di atas. Download ZIP nya,
lalu _extract_ ke folder AmiBroker. Lalu rename direktorinya dari 
`quant-id.master` menjadi `quant.id`.

Langkah-langkah detil untuk _download_ dan _extract_ adalah sbb:
1. Klik **Download ZIP** dari tombol **"Clone or download"** yang berwarna hijau
   di atas, simpan ZIP nya ke Desktop.
2. Setelah terdownload sempurna, double-click file `quant.id-master.zip` yang
   ada di desktop (atau klik kanan dan pilih **Open**).
3. Drag-and-drop folder `quant-id.master` yang ada di dalam ZIP ke direktori
   AmiBroker (`C:\Program Files\AmiBroker`).
4. Rename folder `quant-id.master` menjadi `quant.id`.
5. Sekarang seharusnya Anda punya folder `C:\Program Files\AmiBroker\quant.id` 
   yang isinya `afl`, `charts`, dsb. Jangan sampai folder `quant.id`
   isinya `quant-id.master` misalnya. Kalau sampai begitu, cek kembali sesuai 
   dengan langkah2 di atas.


## Opsional: Menampilkan quant.id Dalam Daftar Charts AmiBroker

Untuk mudahkan pengeditan atau pemakaian AFL dari _quant.id_, Anda bisa menambahkan 
`quant.id` dalam tab pane _Charts_ AmiBroker, dengan cara membuat _symbolic link_
ke direktori `quant.id` dalam direktori `C:\Program Files\AmiBroker\Formulas`.

Kalau Anda skip langkah ini juga tidak apa-apa, karena Anda masih bisa mengedit AFL
dengan cara meng-edit chart.

Anda harus melakukan ini dengan *Command Prompt* yang dibuka sebagai *Administrator*.
Cari icon *Command Prompt* dari _Start Menu_, lalu klik kanan, pilih *Run as Administrator*.
Lalu:

```
cd "\Program Files\AmiBroker\Formulas"

mklink /D quant.id ..\quant.id
```


