import csv

# Nombres de los archivos
input_file = "Libro2.csv"  # Nombre del archivo a copiar
output_file = "Libro1.csv"  # Nombre del archivo de base

# Leer y procesar el archivo
unique_rows = set()  # Para almacenar las filas únicas

with open(input_file, mode="r", newline="", encoding="utf-8") as infile:
    reader = csv.reader(infile)
    header = next(reader)  # Leer la primera fila como encabezado
    processed_rows = [header[:10]]  # Mantener las primeras 10 columnas del encabezado

    for row in reader:
        row_10_columns = tuple(row[:10])  # Convertir a tupla para almacenar en el conjunto
        if row_10_columns not in unique_rows:
            unique_rows.add(row_10_columns)
            processed_rows.append(row[:10])  # Agregar la fila única

# Guardar el archivo con filas únicas
with open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(processed_rows)

print(f"Archivo guardado como {output_file} con filas únicas basadas en las primeras 10 columnas.")
