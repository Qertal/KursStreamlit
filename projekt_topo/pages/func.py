import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

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

def kula(typ, metryka, srodek_x, srodek_y, promien):
    if typ not in ['domknieta','otwarta','sfera']:
        raise ValueError("Typ musi być 'domknieta', 'otwarta' lub 'sfera'")
    
    if metryka > 0 and metryka < 1:
        X, Y = np.meshgrid(np.arange(-(promien**(1/metryka))+srodek_x, promien**(1/metryka)+srodek_x, 0.01), np.arange(-promien**(1/metryka)+srodek_y, promien**(1/metryka)+srodek_y, 0.01))
    else:
        X, Y = np.meshgrid(np.arange(-(promien)+srodek_x, promien+srodek_x, 0.01), np.arange(-promien+srodek_y, promien+srodek_y, 0.01))
        
    points = np.stack([X.ravel(), Y.ravel()], axis=1)
    if metryka > 0 and metryka < 1:
        dists = np.sum(np.abs(points - np.array([srodek_x, srodek_y]))**metryka, axis=1)
    elif metryka >= 1:
        dists = np.sum(np.abs(points - np.array([srodek_x, srodek_y]))**metryka, axis=1)**(1/metryka)
    elif metryka == float('inf'):
        dists = np.max(np.abs(points - np.array([srodek_x, srodek_y])), axis=1)


    if typ == 'domknieta':
        mask_int = dists <= promien
        mask_border = (np.abs(dists - promien) < 0.001)
        interior = points[mask_int]
        border = points[mask_border]
        relative = border - np.array([srodek_x, srodek_y])
        angles = np.arctan2(relative[:, 1], relative[:, 0])
        order = np.argsort(angles)  
        selected = border[order]

        plt.scatter(interior[:, 0]+srodek_x, interior[:, 1]+srodek_y, s=1, color='blue', alpha=1)
        plt.plot(selected[:, 0]+srodek_x, selected[:, 1]+srodek_y, linestyle='solid', color='blue')
        plt.legend(['Kula domknięta'], loc='upper right')


    elif typ == 'otwarta':
        mask_int = dists <= promien
        mask_border = (np.abs(dists - promien) < 0.001)
        interior = points[mask_int]
        border = points[mask_border]
        relative = border - np.array([srodek_x, srodek_y])
        angles = np.arctan2(relative[:, 1], relative[:, 0])
        order = np.argsort(angles)  
        selected = border[order]

        plt.scatter(interior[:, 0]+srodek_x, interior[:, 1]+srodek_y, s=1, color='blue', alpha=1)
        plt.plot(selected[:, 0]+srodek_x, selected[:, 1]+srodek_y, linestyle='dashed', color='red')
        plt.legend(['Wnętrze kuli', 'Brzeg kuli'], loc='upper right')



    elif typ == 'sfera':
        mask_border = (np.abs(dists - promien) < 0.01)
        border = points[mask_border]
        relative = border - np.array([srodek_x, srodek_y])
        angles = np.arctan2(relative[:, 1], relative[:, 0])
        order = np.argsort(angles)  
        selected = border[order]
        plt.plot(selected[:, 0]+srodek_x, selected[:, 1]+srodek_y, linestyle='solid', color='blue')
        plt.legend(['Sfera'], loc='upper right')

    plt.axis('equal')
    plt.title(f"{'Sfera' if typ == 'sfera' else 'Kula ' + typ} o środku w punkcie {srodek_x, srodek_y}, promieniu {round(promien,2)} przy metryce (Minkowskiego p={round(metryka, 2)})")
    # plt.show()
    st.pyplot(plt.gcf())