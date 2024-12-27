# Mover las fotos de kaggle a la carpeta de las manos para poder ir leyéndolas al vuelo

from pathlib import Path
import shutil as st
import polars as pl

path = Path('/home/pablo/Desktop/tercero/mdp/trabajo/imagenes_kaggle/Hands/Hands')

schema = {
    "id": pl.Utf8,                # ID como cadena de texto
    "age": pl.Int32,              # Edad como entero
    "gender": pl.Utf8,            # Género como cadena de texto
    "skinColor": pl.Utf8,         # Color de piel como cadena de texto
    "accessories": pl.Int32,      # Accesorios como entero (0 o 1)
    "nailPolish": pl.Int32,       # Esmalte de uñas como entero (0 o 1)
    "aspectOfHand": pl.Utf8,      # Aspecto de la mano como cadena de texto
    "imageName": pl.Utf8,         # Nombre de la imagen como cadena de texto
    "irregularities": pl.Int32    # Irregularidades como entero (0 o 1)
}

def posicion_mano(s: str) -> str:
    if s == 'dorsal right':
        resul = 'RB'
    elif s == 'dorsal left':
        resul = 'LB'
    elif s == 'palmar right':
        resul = 'RF'
    elif s == 'palmar left':
        resul = 'LF'
    return resul

dataset = pl.read_csv('/home/pablo/Desktop/tercero/mdp/trabajo/imagenes_kaggle/HandInfo.csv', schema=schema)

dataset = (
    dataset
    .with_columns(pl.col('aspectOfHand').map_elements(posicion_mano, return_dtype=str).alias('Posición Mano'))
    .select([pl.col('Posición Mano'), pl.col('imageName')])
)

cont = 200

for im in path.iterdir():
    im_name = str(im).split('/')[-1]
    pos = dataset.filter(pl.col("imageName") == im_name)["Posición Mano"].item()
    if cont < 1000:
        new_name = '0' + str(cont) + '_' + pos + '.jpg'
    else:
        new_name = str(cont) + '_' + pos + '.jpg'
    dst = '/home/pablo/Desktop/tercero/mdp/trabajo/HANDS/' + new_name
    st.copy(im, dst)
    print((cont-200)/len(dataset))
    cont += 1