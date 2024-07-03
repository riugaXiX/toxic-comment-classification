import numpy as np

# Data Anda
data = [
    ("berani nagih pajak keamanan non peribumi habib rizieq anies amien rais hansi mereka rizieq anies amp amin golongan kelas ii asia membantu peribumi indonesia merebut kemerdekaan penjajahan belanda dnnso ngapain peribumi nagih pajak amazed nmereka teman d nnbeda si sipit golongannya mengkhianati bangsa ngakaks nn wakaka", 0, 1, 0, 0),
    ("basherrl heh kontol jan sok pemes rp muka kek memek org tua kek monyet agama aje agama kontol", 1, 0, 0, 1),
    ("colok memek pke kontol psti bkin smangat cewedodol bete kamar tiduran uuh badany gak enak ngapain", 1, 0, 0, 0),
    ("ehh emang terblokir pakai hape android situs diakses mentri tolol fuck", 0, 0, 0, 1),
    ("bunuh kafir harby tepatnya jokohq ayo sodara tertarik bunuh orang sumbangkan duit via hafidz ary mudahan barokah", 0, 0, 1, 1),
    ("khilafah adl akad akadakad dipehuni hai orangorang beriman penuhilah akadakad q almaidah", 0, 0, 1, 0),
    ("ahelah muslim membunuh kafir tragedi sept bom bali dll muslim membunuh muslim suriah yemen dll playing victim at it finest", 0, 1, 1, 1),
    ("millennisha kali anjing ngaku goblok gak bacot njing gak ngaku salah lo ngatain", 0, 0, 0, 1),
    ("bunuh mah dapet pahala ngurangin orang kafir tertawa denisarisari dosaa d fnh usir bunuh", 0, 1, 1, 1),
    ("joke orang cina kl nntn sporting event lawan china ganyang cina mngkn gak lucu kl org teriak nontonthomas sayajugacina fb", 0, 1, 1, 1)
]

# Pisahkan teks dan label
texts = [item[0] for item in data]
labels = np.array([item[1:] for item in data])
