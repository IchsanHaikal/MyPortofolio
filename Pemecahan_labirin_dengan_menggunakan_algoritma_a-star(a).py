#Kelompok 4 - Algoritma A-Star untuk Memecahkan Labirin
#Import library yg diperlukan
from pyamaze import maze, agent, textLabel
from queue import PriorityQueue

#Function h(n) -> Jarak Manhattan antara cell1 (sel n) dan cell2 (sel tujuan)
def h(cell1, cell2):
    x1, y1 = cell1 #(x,y) merupakan koordinat n
    x2, y2 = cell2 #(x,y) merupakan koordinat tujuan

    """
    Mengembalikan nilai selisih antara koordinat n dengan koordinat tujuan,
    serta menjumlahkannya
    """
    return abs(x1 - x2) + abs(y1 - y2)

#Function A*
def aStar(m):
    #Sel awal 
    start = (m.rows, m.cols)

    #Nilai g(n) awal
    g_score = {cell:float('inf') for cell in m.grid}
    g_score[start] = 0
    #Nilai f(n) awal
    f_score = {cell:float('inf') for cell in m.grid}
    f_score[start] = h(start, (1,1))

    #Method untuk memprioritaskan item antrian
    open = PriorityQueue()

    open.put((h(start,(1,1)), h(start,(1,1)), start))

    #Variable untuk menyimpan nilai jalur berdasarkan koordinatnya
    aPath = {}

    while not open.empty():
        currCell = open.get()[2]

        if currCell == (1,1):
            break

        #Direction (East, South, North, West)
        for d in 'ESNW':
            if m.maze_map[currCell][d] == True:
                if d == 'E':
                    childCell = (currCell[0], currCell[1]+1)
                if d == 'W':
                    childCell = (currCell[0], currCell[1]-1)
                if d == 'N':
                    childCell = (currCell[0]-1, currCell[1])
                if d == 'S':
                    childCell = (currCell[0]+1, currCell[1])

                #g(n) nilai actual untuk mencapai sel tujuan dari sel n
                temp_g_score = g_score[currCell] + 1
                #f(n) = g(n) + h(n)
                temp_f_score = temp_g_score + h(childCell, (1,1))

                if temp_f_score < f_score[childCell]:
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_f_score
                    open.put((temp_f_score,h(childCell, (1,1)), childCell))
                    aPath[childCell] = currCell

    #Variable untuk menyimpan nilai jalur ke depan dari sel awal menuju sel tujuan
    fwdPath = {}

    #Sel tujuan
    cell = (1,1)

    #Selama sel tujuan tidak sama dengan sel awal
    while cell != start:
        #Maka: dilakukan perhitungan fwdPath
        fwdPath[aPath[cell]] = cell
        cell = aPath[cell]

    #Mengembalikan nilai untuk jalur ke depan dari sel awal menuju sel tujuan
    return fwdPath

"""
Menjalankan sebuah kemungkinan dengan 
method __init__
"""
if __name__ == '__main__':
    m = maze(20,40) #Mengatur ukuran maze map 20x40
    m.CreateMaze()  #Membuat maze map
    path = aStar(m) #Memanggil function aStar(m)

    #Digunakan untuk membuat 'agen'
    a = agent(m, footprints = True)
    #'Agen' tersebut akan menelusuri jalur yang dihitung oleh function aStar(m)
    m.tracePath({a:path})
    #Keterangan untuk jumlah jalur yg dipilih
    l = textLabel(m,'A Star Path Length',len(path)+1)

    #Menjalankan maze
    m.run()