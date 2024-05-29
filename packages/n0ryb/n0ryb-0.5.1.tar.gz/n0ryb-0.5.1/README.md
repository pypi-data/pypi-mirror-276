# Hack4u Academy Prueba
Una biblioteca de prueba python para consultar cursos en hack4u.

## Curso Disponibles:

- Introduccion a linux [15 horas]
- Introduccion al hacking [53 horas]
- Personalizacion de linux [3 horas]

## Instalacion 

Instala el paquete usando `pip3`:
```python3
pip3 install n0ryb
```

## Uso basico

### Listar todos los cursos

```python

from n0ryb import list_courses
for course in list_courses():
    print(course)
```

# Obtener un curso por nombre

```python
from n0ryb import search_course
course =  search_course("Introduccion a linux")
print(course)
```

### Calcular duracion total de los cursos 
```python3

from n0ryb.utils import total_duration


print(f"Duracion Total: {total_duration()} horas")




