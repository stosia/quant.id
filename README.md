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

# General Rules

**Jangan memakai/meng-edit file-file yang ada di direktori _internal_**

**Isi formula dalam chart sebaiknya cuma meng-include indicator asalnya**

**Sesuaikan isi file .chart**

Kalau Anda membuat chart/sheet/pane baru, maka Anda harus edit file .chartnya secara
manual dengan editor teks agar isinya rapih seperti asalnya, dan agar ketika digunakan
nanti tidak akan menghasilkan file "\_imported".

**Masukkan kode dalam chart dalam section**

# Cara Membuat Indicator Baru

Buatlah seperti biasa, dan simpan di folder `quant.id\\Indicators\\..`.

# Cara Menambah Indicator dalam Chart

Kalau Anda cuma memakai chart untuk kepentingan pribadi, silakan menambah-nambah chart
sesuka Anda sesuai petunjuk AmiBroker pada umumnya.

Tapi kalau Anda berniat untuk men-share kembali modifikasi Anda atau menyumbangkan ke
repository quant.id, maka Anda harus mengikuti langkah-langkah berikut dengan seksama.
Ribet memang, tapi ribetnya sekali doang dan yang ribet developernya. Sedangkan orang-
orang dan developer-developer lain yang memakai chartnya nanti akan lebih hepi.

Langkah-langkahnya:

1. Double-click indicatornya agar ditambahkan dalam pane baru di chart dan sheet yang
   sedang aktif.
2. Right click di indicator yang baru ditambahkan di chart (bukan indicator
   yang ada di daftar indicator di sebelah kiri), lalu pilih **Edit**. Ubah formulanya
   sehingga isinya menjadi ini:
```
//
// DO NOT EDIT THIS FILE. EDIT THE FILE IN THE INCLUDE BELOW INSTEAD.
//

#include_once <..\..\quant.id\Indicators\ForeignFlow\ForeignFlow_Price.afl>
```

   Ubah isi file dalam _include_ ke lokasi indicator yang barusan Anda tambahkan.

   Tambahkan keterangan copyright dan lisensi. Hanya lisensi GPL versi 2 atau yang lebih
   baru yang diperbolehkan kalau Anda ingin file Anda dimasukkan dalam repository.
3. Bikin formula baru di direktori `internal` yang ada di direktori tempat file
   chart berada. Namakan file ini sama seperti nama indicatornya. Dan isinya copy paste
   dari apa yang Anda tulis di step no 2 di atas. Save formulanya, lalu tutup window
   editornya.
4. Save chart, lalu tutup chart, dan exit AmiBroker (kalau tidak exit, maka ada
   kemungkinan AmiBroker akan menyimpan chart dalam cache sehingga hasil editan
   kita nanti (di step berikutnya) akan tertimpa).
5. Edit file chartnya (file yang berekstensi `.chart`) dengan editor teks misalnya
   Notepad.
6. Cari pane yang baru Anda tambahkan. Salah satu cirinya, **FilePath**-nya biasanya
   ada di direktori `Formulas\Drag-Drop` dari AmiBroker. Ganti isi **FilePath**
   dengan lokasi dari file formula yang Anda bikin di step 3. Misalnya:
   `<FilePath>quant.id\\Charts\\ForeignFlow\\internal\\ForeignFlow_NetVol.afl</FilePath>`
   Lihat pane-pane yang lain untuk contoh. Save file .chart nya dan exit editor.
7. Buka lagi AmiBroker, dan buka chartnya. Lalu cek pakai Windows Explorer untuk
   memastikan AmiBroker tidak membuat file `_imported` di direktori `internal`.
 



# FAQ

**Q: Kenapa isi formula chart cuma meng-_include_ formula lain?**

A: Format chart AmiBroker yang baru (yang berekstensi .chart) cukup membuat pusing.

Biar nggak pusing dengan file-file "\_imported" yang terjadi kalau kita meng-_edit_
   chartnya, atau kehilangan perubahan kalau lupa save chart. Dan agar kalau ada perubahan
   di suatu indicator, maka perubahan itu langsung terupdate di chart-chart lain yang 
   memakai indicator yang sama. 

