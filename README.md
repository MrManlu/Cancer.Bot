![# Cancer.Bot - Clasificación de imágenes histológicas para la detección de cáncer de mama](https://raw.githubusercontent.com/MrManlu/Cancer.Bot/master/IMG/CancerBot.png)

## Sobre el proyecto
Este repositorio contiene el proyecto de fin de curso realizado durante las clases de [Saturdays.AI][SatAI] realizadas en Sevilla durante el curso 2019. Otros proyectos presentados pueden encontrarse en [su repositorio de GitHub][SAGit]

El proyecto consiste en la clasificación de imágenes médicas tomadas en pruebas histológicas sobre tejido mamario, haciendo uso de modelos predictivos (inteligencia artificial). Nos centraremos en la detección del **Carcinoma Ductal Invasivo**, el tipo más común de cáncer de mama.


Como entrada, el programa toma una imagen histológica de alta resolución, dividida previamente en pequeñas muestras de 50x50 píxeles. Tras procesar y clasificar cada muestra, el programa recompondrá la imagen original para la rápida identificación de las zonas afectadas por parte del usuario.

El modelo predictivo, así como el código fuente para la generación del *dataset* y para el entrenamiento de la red pertenecen a **Adrian Rosebrock** (*autor del blog [PyImageSearch][PyBlog]*)

El sistema está basado en el tutorial [*Breast cancer classification with Keras and Deep Learning*][PBBreast], por el cual el proyecto tiene la misma estructura de archivos y carpetas.

## Datos técnicos

- Dataset (Kaggle): [Breast Histopathology Images][DS] (por *Paul Mooney*)
- Modelo predictivo: **CancerNet** (por *Adrian Rosebrock*)
- Equipo de entrenamiento:
    - CPU: Intel® Core™ i3-4170 CPU @ 3.70GHz × 4
    - GPU: GeForce GTX 1050/PCIe/SSE2
    - S.O.: Ubuntu 18.04.3 LTS
    - RAM: 8 GB

- Tiempo de entrenamiento: 24 horas aprox.
    - Generaciones: 40
    - Modelos generados: 38

## Prerrequisitos
Debemos tener instalada una versión actualizada de Python 3. Se ha utilizado Python 3.6.8 durante éste tutorial.

Las librerías necesarias son las expuestas en el [blog de Adrian][PBBreast], además de algunas adicionales:

- OpenCV: `pip3 install opencv-python`
- Glob: `pip3 install glob3`

## Puesta en marcha
Para ejecutar el proyecto, debemos descargar el [dataset][DS] desde Kaggle y descomprimirlo.

El dataset consiste en imágenes de muy alta resolución, ordenadas en carpetas con un número que identifica a cada paciente (por ejemplo, `8867`). Cada imagen está dividida en pequeñas muestras de 50x50 píxeles, las cuales estarán dentro de la carpeta `'0'` o `'1'` si son **negativas** o **positivas** respectivamente.

Archivos:

- **show_image.py**: Abre una imagen del dataset y la reconstruye. Muestra la imagen original, y si se pulsa cualquier tecla, se muestra la imagen marcada **por el especialista** como **zona positiva**. Además, guarda las imágenes en la carpeta donde es ejecutado.

    - Sintaxis: `python3 show_image.py /<DatasetFolder>/<ID>`

    - Ejemplo de uso: `python3 show_image.py datasets/orig/8867`

- **eval_image.py:** Evalúa, según el modelo predictivo previamente entrenado, una imagen dada por el ID de un paciente. Genera cuatro archivos:

    - `<ID>-orig.jpg`: Imagen original reconstruida.
    - `<ID>-true.jpg`: Imagen original, con zona positiva marcada por el especialista.
    - `<ID>-pred.jpg`: Imagen marcada por probabilidades. Las zonas más marcadas serán las más propensas a ser positivas.
    - `<ID>-prth.jpg`: Imagen marcadas con las zonas cuyas probabilidades superen un umbral del **85%**.
        - Este valor es configurable, pudiéndose editar mediante la variable `threshold` dentro del propio archivo.

    - Sintaxis: `python3 show_image.py /<DatasetFolder>/<ID>`

    - Ejemplo de uso: `python3 show_image.py datasets/orig/8867`

## Entrenamiento
En caso de querer entrenar a la red en nuestro popio equipo, debemos segir las instrucciones del [blog de Adrian][PBBreast].

Se adjuntan el archivo modificado `train_model.py`, el cual realiza la misma función que el archivo ofrecido por Adrian, con la diferencia de que **a la vez que entrena, guarda el modelo entrenado si ha habido alguna mejoría en los resultados.** Así se han generado los archivos de la carpeta `models`, correspondientes a las generaciones que han ido mejorando los resultados.

## Resultados
```
              precision    recall  f1-score   support

           0       0.90      0.90      0.90     39847
           1       0.75      0.75      0.75     15658

    accuracy                           0.86     55505
   macro avg       0.83      0.82      0.83     55505
weighted avg       0.86      0.86      0.86     55505

[[36028  3819]
 [ 3980 11678]]
acc: 0.8595
sensitivity: 0.9042
specificity: 0.7458
```

## Autores

- Jesús Antonio de la Fuente Lozano
- Manuel Luis Alcázar Laynez

## Referencias

- [Saturdays.AI][SatAI]
    - [Repositorio de GitHub][SAGit]

- [PyImageSearch][PyBlog]
    - [Breast cancer classification with Keras and Deep Learning][PBBreast]

- [Breast Histopathology Images][DS] - Kaggle dataset
- [OpenCV](https://opencv.org/)

[SatAI]: https://www.saturdays.ai/
[SAGit]: https://github.com/SaturdaysAI/Projects
[PyBlog]: https://www.pyimagesearch.com/
[PBBreast]: https://www.pyimagesearch.com/2019/02/18/breast-cancer-classification-with-keras-and-deep-learning/
[DS]: https://www.kaggle.com/paultimothymooney/breast-histopathology-images
