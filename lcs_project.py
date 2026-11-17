# Generar cadenas de textos aleatorios.
import random
# Calcular cuánto tarda el equipo en ejecutar cada versión del
# algoritmo.
import time
# Medir cuánta memoria consume el algoritmo.
import tracemalloc

# VERSIÓN A: Recursiva Directa (Sin memorización.
# Complejidad Temporal: O(2(m+n)) | Espacio: O(m + n) por la pila.

# Definir las cadenas de texto a comparar X e Y. Nº caracteres para # la cadena X (m) y para la cadena Y (n).
def lcs_recursive(X, Y, m, n):
  # Comprobar si alguna cadena se ha quedado sin caracteres.
  if m == 0 or n == 0:
    return 0
  # Comparar el último carácter actual de X con el último de Y.
  if X[m - 1] == Y[n - 1]:
  # Si son iguales suma 1 al resultado y reduce el tamaño de las 
  # cadenas en uno.
    return 1 + lcs_recursive(X, Y, m - 1, n - 1)
  # Si no explora los dos caminos y se queda con el mayor max(), 
  # descarta el último carácter de Y y de X lcs().
  else:
    return max(lcs_recursive(X, Y, m, n - 1), lcs_recursive(X, Y, m - 1, n))

# VERSIÓN B: Algoritmo de Hirschberg (Divide y Vencerás)
# Espacio O(m + n), Tiempo O(m * n)

# Calcula la últmia fila de la tabla de programación dinámica.
def get_lcs_row(X, Y):
  m, n = len(X), len(Y)
  prev = [0] * (n + 1)
  for i in range(1, m + 1):
    curr = [0] * (n + 1)
    for j in range(1, n + 1):
      if X[i - 1] == Y[j - 1]:
        curr[j] = prev[j - 1] + 1
      else:
        curr[j] = max(prev[j], curr[j - 1])
    prev = curr
  return prev

# Divide y vencerás de forma recursiva.
def lcs_hirschberg(X, Y):
  A = len(X)
  B = len(Y)
  if A == 0: return ""
  if A == 1: return X[0] if X[0] in Y else ""
  # Divide la cadena X por la mitad X1 y X2.
  mid = A // 2
  X1 = X[:mid]
  X2 = X[mid:]
  # Calcula los puntuajes de LCS desde el inicio de X1 hasta el final 
  # de Y.
  L1 = get_lcs_row(X1, Y)
  # Calcula los puntuajes de LCS desde el final de X2 hasta el inicio 
  # de Y.
  L2 = get_lcs_row(X2[::-1], Y[::-1])[::-1]
  # 
  max_val = -1
  split_j = 0
  for j in range(B + 1):
    val = L1[j] + L2[j]
    if val > max_val:
      max_val = val
      split_j = j
  Y1 = Y[:split_j]
  Y2 = Y[split_j:]
  return lcs_hirschberg(X1, Y1) + lcs_hirschberg(X2, Y2)

# VERSIÓN C: Programación Dinámica Tabular
# Espacio O(m * n), Tiempo O(m * n) 

def lcs_tabular(X, Y):
  m, n = len(X), len(Y)
  dp = [[0] * (n + 1) for _ in range(m + 1)]
  for i in range(1, m + 1):
    for j in range(1, n + 1):
      if X[i - 1] == Y[j - 1]:
        dp[i][j] = dp[i - 1][j - 1] + 1
      else:
        dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
  return dp[m][n]

# BANCO DE PRUEBAS Y EXPERIMENTOS

def run_experiments():
  # Definición de longitudes crecientes (la última >= 1000)
  sizes = [15, 100, 300, 600, 1000]

  print(
      f"{'N (Len)':<10} | {'Versión':<25} | {'Tiempo CPU (s)':<15} | {'Memoria Máx (KB)':<18}"
  )
  print("-" * 75)

  for size in sizes:
    # Generar cadenas aleatorias {'A', 'C', 'G', 'T'}
    alphabet = ['A', 'C', 'G', 'T']
    X = ''.join(random.choices(alphabet, k=size))
    Y = ''.join(random.choices(alphabet, k=size))

    # 1. Versión A (Solo para tamaños pequeños debido a 
    # complejidad exponencial O(2n))
    if size <= 15:
      tracemalloc.start()
      start_time = time.process_time()
      _ = lcs_recursive(X, Y, len(X), len(Y))
      cpu_time = time.process_time() - start_time
      _, peak_mem = tracemalloc.get_traced_memory()
      tracemalloc.stop()
      print(
          f"{size:<10} | {'A - Recursiva':<25} | {cpu_time:<15.6f}| {peak_mem / 1024:<18.2f}"
    )
    else:
      print(
          f"{size:<10} | {'A - Recursiva':<25} | {'TIMEOUT(>1h)':<15} | {'-'}"
      )

    # 2. Versión B (Hirschberg)
    tracemalloc.start()
    start_time = time.process_time()
    _ = lcs_hirschberg(X, Y)
    cpu_time = time.process_time() - start_time
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(
        f"{size:<10} | {'B - Hirschberg':<25} | {cpu_time:<15.6f} | {peak_mem / 1024:<18.2f}"
    )

    # 3. Versión C (Tabular)
    tracemalloc.start()
    start_time = time.process_time()
    _ = lcs_tabular(X, Y)
    cpu_time = time.process_time() - start_time
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(
        f"{size:<10} | {'C - Tabular':<25} | {cpu_time:<15.6f} | {peak_mem / 1024:<18.2f}"
          )
    print("-" * 75)

if __name__ == '__main__':
  random.seed(42)
  run_experiments()