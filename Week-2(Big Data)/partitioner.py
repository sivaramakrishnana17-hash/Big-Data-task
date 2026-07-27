def partition(mapped_data):
    partitioned_data = {}

    for key, value in mapped_data:
        if key not in partitioned_data:
            partitioned_data[key] = []

        partitioned_data[key].append(value)

    return partitioned_data