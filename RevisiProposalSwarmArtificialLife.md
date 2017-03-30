# Proposal Proyek Swarm Artificial Life KB
**Shark and Fish Swarm:
1. Dalam suatu segi empat berukuran MxN, ada kumpulan Fish yang tersusun rapi sebuah tabel, membentuk segiempat dengan ukuran PxQ dimana P<M dan Q<N.
2. Ada beberapa Shark yang diinitialize di suatu koordinat random dalam segi empat MxN dan bergerak dengan rumusan tertentu / hanya bergerak lurus dengan speed yang berbeda dan memantul ketika mengenai batasan
3. Kumpulan Fish menjaga jarak dari Shark sehingga jarak itu membentuk lingkaran dengan radius R. Jika tidak dekat dengan Shark, Fish akan diam di tempat dengan rapi. Jika sempat didekati Shark, namun Shark sudah menjauh, Fish akan kembali ke tempat awalnya, sehingga kumpulan Fish tetap berbentuk segi empat yang rapi. Fish yang didekati Shark bisa menjaga jarak hingga keluar dari kotak PxQ namun tidak lebih dari kotak MxN.

**Diusahakan:
* Fish bergerak dengan rumusan tertentu tanpa ada influence dari global best (Influence dari personal best masih dipertimbangkan) agar Fish tidak bisa bergerak terlalu jauh dari tempat asalnya dalam periode waktu yang pendek, dan jika bergerak biasa tanpa pengaruh Shark, Fish akan dijaga agar tidak keluar dari batasan segi empat PxQ. Rumusan yang digunakan misalnya:
  *f(x,y) = 1 + ((x-5)2(x+5)2 + (y-5)2(y+5)2 - 1)*(0.5*(x+y+25))
* Ada beberapa Fish yang ditetapkan sebagai target. Shark bergerak ke arah target Fish terdekat dimana speed Shark bisa lebih besar ataupun lebih kecil daripada speed Fish menjauhi Shark, tergantung sewaktu Shark diinisialisasi. Jika berhasil mengenai collide dengan Fish target, target diganti.
* Jika suatu Shark tidak berhasil dapat target dalam waktu tertentu, Shark mati karena starvation dan akan diinitialize Shark lain sebagai pengganti.
* Shark dibagi ke dalam 2 tim. Target Fish juga dibagi 2, diperuntukkan untuk 1 tim tertentu. Jika suatu Shark dari tim 1 berhasil collide dengan Fish target tim mereka, maka salah 1 target Fish tim lawannya akan pindah ke Fish lain secara random dengan harapan mengulur waktu agar Shark mati (misalnya fish nomor 23 adalah target awal, namun karena diganti maka targetnya sekarang nomor 84) 
