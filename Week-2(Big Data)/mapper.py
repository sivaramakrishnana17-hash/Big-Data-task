def mapper(data):
    mapped_data = []

    for line in data:
        genre = line.strip()

        if genre:
            # Emit key-value pair
            mapped_data.append((genre, 1))

    return mapped_data