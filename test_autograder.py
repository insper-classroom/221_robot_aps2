import pytest
import cv2
import fotogrametria
from webcam import calcular_angulo_e_distancia_na_image_da_webcam

segmentado_ciano = None
segmentado_magenta = None
ccontorno_ciano = None
contorno_magenta = None 
centro_ciano = None
centro_magenta = None
        

## PARTE 1 - FOCO
def test_foco():
    resp = 629.9212598425197
    assert resp * 0.9 <= fotogrametria.encontrar_foco(80,12.70,100) <= resp * 1.1, "PARTE 1 - foco resultante está incorreto"

## PARTE 2 - SEGMENTAR
def test_segmentar():    
    img = cv2.imread("notebook_aux/folha_atividade.png")
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    global segmentado_ciano
    global segmentado_magenta
    segmentado_ciano = fotogrametria.segmenta_circulo_ciano(hsv)
    segmentado_magenta = fotogrametria.segmenta_circulo_magenta(hsv)

## PARTE 3 - CONTORNO
def test_contour():
    global ccontorno_ciano
    global contorno_magenta

    # Area Ciano: 591888.0 - Area Magenta: 591835.0
    rc = 591888.0 
    rm = 591835.0

    ccontorno_ciano = fotogrametria.encontrar_maior_contorno(segmentado_ciano)
    contorno_magenta = fotogrametria.encontrar_maior_contorno(segmentado_magenta)

    assert rc * 0.9 <= cv2.contourArea(ccontorno_ciano) <= rc * 1.1, "PARTE 3 - contorno_ciano esta incorreto"
    assert rm * 0.9 <= cv2.contourArea(contorno_magenta) <= rm * 1.1, "PARTE 3 - contorno_magenta esta incorreto"

## PARTE 4 - CENTRO
def test_centro():
    img = cv2.imread("notebook_aux/folha_atividade.png")

    # Centro Ciano: (1079, 2802) - Centro Magenta: (1080, 816)
    global centro_ciano
    global centro_magenta
    centro_ciano = fotogrametria.encontrar_centro_contorno(ccontorno_ciano)
    centro_magenta = fotogrametria.encontrar_centro_contorno(contorno_magenta)
    img_4 = cv2.circle(img,centro_ciano, 10, (255,255,255), -1)
    img_4 = cv2.circle(img_4,centro_magenta, 10, (255,255,255), -1)

    x,y = centro_ciano
    assert min(img_4[y][x] == [255,255,255]), "PARTE 4 - centro_ciano esta incorreto"
    x,y = centro_magenta
    assert min(img_4[y][x] == [255,255,255]), "PARTE 4 - centro_magenta esta incorreto"

## PARTE 5 - FOCO
def test_outrofoco():
    # h = 1986.0002517623204 - f = 1014.1732283464568
    rh = 1986.0002517623204
    rf = 1014.1732283464568
    h = fotogrametria.calcular_h(centro_ciano, centro_magenta)
    f = fotogrametria.encontrar_foco(80,12.70,161.0)

    assert rh * 0.9 <= h <= rh * 1.1, "PARTE 5 - h esta incorreto"
    assert rf * 0.9 <= f <= rf * 1.1, "PARTE 5 - f esta incorreto"

## PARTE 6 - DISTANCIA
def test_distance():
    img_test = cv2.imread("img/test01.jpg")
    # d = 40.124415891157206
    dr = 40.124415891157206
    h, centro_ciano, centro_magenta, contornos_img = fotogrametria.calcular_distancia_entre_circulos(img_test)
    f = fotogrametria.encontrar_foco(80,12.70,161.0)
    d = fotogrametria.encontrar_distancia(f,12.70,h)
    assert dr * 0.9 <= d <= dr * 1.1, "PARTE 6 - Incorreto"

## PARTE 7 - ANGULO
def test_angle():
    img_test = cv2.imread("img/angulo04.jpg")
    # angulo = 28.56758430890487
    ra = 28.56758430890487

    h, centro_ciano, centro_magenta, contornos_img = fotogrametria.calcular_distancia_entre_circulos(img_test)
    f = fotogrametria.encontrar_foco(80,12.70,161.0)
    d = fotogrametria.encontrar_distancia(f,12.70,h)
    angulo = fotogrametria.calcular_angulo_com_horizontal_da_imagem(centro_ciano, centro_magenta)
    assert ra * 0.9 <= abs(angulo) <= ra * 1.1, "PARTE 7 - Incorreto"
        
## PARTE 8 - WEBCAM
def webcam_test():
    # distancia = 40.25589729191707 - angulo = 28.56758430890487
    ra = 28.56758430890487
    dr = 40.25589729191707 
    img_test = cv2.imread("img/angulo04.jpg")
    img, distancia, angulo = calcular_angulo_e_distancia_na_image_da_webcam(img_test, 1014.1732283464568)
    assert ra * 0.9 <= abs(angulo) <= ra * 1.1, "PARTE 8 - ângulo incorreto: %f" % angulo
    assert dr * 0.9 <= distancia <= dr * 1.1, "PARTE 8 - distância incorreta: %f" % distancia
        
if __name__ == "__main__":
    test_foco()
    test_segmentar()
    test_contour()
    test_centro()
    test_outrofoco()
    test_distance()
    test_angle()
    webcam_test()
    

