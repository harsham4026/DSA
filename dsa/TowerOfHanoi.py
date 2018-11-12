def TowerOfHanoi(numOfDisks, from_rod, to_rod, aux_rod):
  if numOfDisks == 1:
    print ("the disk 1 is moved from ", from_rod, "to rod ",to_rod)
    return
  TowerOfHanoi(numOfDisks-1, from_rod, aux_rod, to_rod)
  print("moving the disk " ,numOfDisks, " from_rod ",from_rod, " to rod ", to_rod)
  TowerOfHanoi(numOfDisks-1, aux_rod, to_rod, from_rod)

if __name__ == '__main__':
  n=10
  TowerOfHanoi(n, 'A', 'B', 'C')