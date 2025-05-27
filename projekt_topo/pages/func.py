import numpy as np

def metryka_minkowskiego(x,y,p):
    if p >=1 and p != float('inf'):
        wynik = (np.sum((abs(x-y))**p))**(1/p)
    elif p < 1 and p >= 0:
        wynik = np.sum(abs((x-y))**p)
    elif p == float('inf'):
        wynik = np.max(abs(x-y))
    return wynik

def macierz_odleglosci(x,p):
    rozmiar = len(x)
    D = np.zeros((rozmiar,rozmiar))
    for i in range(len(x)):
        for j in range(i,len(x)):
            D[j,i] = D[i,j] = metryka_minkowskiego(x[i],x[j],p)
    # return print(f"Macierz odległości dla p = {p} wygląda następująco:\n{np.round(D,2)},\na średnica zbioru:\n{np.max(D)}")
    return D, np.max(D)  # dla macierzy odległości


def odleglosc_miedzy_zbiorami(x,y,p):
    rozmiar_x = len(x)
    rozmiar_y = len(y)
    D = np.zeros((rozmiar_x,rozmiar_y))
    for i in range(len(x)):
        for j in range(len(y)):
            D[i,j] = metryka_minkowskiego(x[i],y[j],p)
    # return print(f'Odległośc dla p = {p} między tymi zbiorami wynosi:\n{np.min(D)}')
    return np.min(D)  # dla odległości między zbiorami

def macierz_do_latex(D):
    wiersze = [
        " & ".join(f"{val:.2f}" for val in row)
        for row in D
    ]
    latex = "D(X) = \\begin{bmatrix}\n" + " \\\\\n".join(wiersze) + "\n\\end{bmatrix}"
    return latex