# IA_BD_M1_UD1_PracticaLaberint

## Descripció de la pràctica
Aquesta pràctica consisteix a codificar un problema senzill de cerca emprant un enfocament
declaratiu basat en la lògica proposicional.  
Per tal de solucionar fàcilment el problema farem us de «Solvers» per el problema SAT i de la seva contrapart per optimització, el problema MaxSAT.  
El problema que solucionarem consisteix a trobar alguna ruta des del punt inicial cap algun dels objectius finals del laberint.

## Dependències
* [Python](https://www.python.org/downloads/)
* Mòdul de Python [PySAT](https://pysathq.github.io/)
```
$ pip install python-sat
```
* Mòdul de Python [PyPNG](https://pypng.readthedocs.io/en/latest/ex.html)
```
$ pip install pypng
```

## Execució del programa
L'execució es fa a través de l'script `maze_solver.py`, passant com a paràmetre l'identificador de l'experiment (número) i opcionalment la ruta d'un arxiu de laberint per utilitzar en comptes del laberint per defecte.

### Experiments disponibles:
1. Experiment SAT que genera un camí de **doble direcció** amb restriccions de **cardinalitat manual**
2. Experiment SAT que genera un camí de **doble direcció** amb restriccions de **cardinalitat de PySAT**
3. Experiment SAT que genera un camí d'**una direccio** utilitzant **diferents capes** del mateix laberint
4. Experiment MaxSAT que genera un camí de **doble direcció** amb restriccions de **cardinalitat manual**
5. Experiment MaxSAT que genera un camí de **doble direcció** amb restriccions de **cardinalitat de PySAT**
6. Experiment MaxSAT que genera un camí d'**una direccio** utilitzant **diferents capes** del mateix laberint

### Arxius de laberint
> Dins la carpeta `./data/` es troben un seguit d'exemples d'arxius de laberint  

Dins la pràctica s'utilitza l'extensió `.mz` per aquest tipus d'arxius, però es pot utilitzar qualsevol arxiu de text pla.  
L'estructura de l'arxiu es la següent:
* Primera linea: un seguit de 4 caràcters que definiran, en ordre, l'usuari, els objectius, els camins i les parets.
* Seguents linies: la representació del laberint utilitzant els caràcters definits a la primera linia.

Un exemple d'arxiu de laberint que representa el laberint per defecte:
```
uo #
o######o
    #   
 ## # # 
  # # # 
# #     
# ######
        
#### ###
u    #  
```

## Configuració del programa
Per canviar el funcionament de l'script es pot modificar l'arxiu `constants.py`.  
Dins l'arxiu ja està definit que fa cada variable, però de forma genèrica es pot modificar:
* Generar arxius de dades
* Veure diferents representacions del laberint
* Veure informació extra de la resolució del laberint
* Forçar un cicle dins el laberint
* Canviar les caselles utilitzades per generar un cicle.

Hi ha també la opció de canviar el laberint per defecte i la llista d'experiments, però es recomana no canviar aquests paràmetres.

## Utilitats
Existeixen dos scripts d'utilitat:
* `maze_representator.py`: mostra un laberint amb una solucio passada com a paràmetre (.json amb el model) i opcionalment un arxiu de laberint.
* `maxhs_model_parser.py`: genera un arxiu de model (.json) a partir de una solució donada per MaxHS passada com a paràmetre a travès d'un arxiu de text pla amb 0s i 1s.
* `maxcdcl.py`: necesita el binari de maxcdcl al mateix directori, l'executa y compta el temps d'execució
* `maxhs.py`: necesita el binari de maxhs al mateix directori, l'executa y compta el temps d'execució
