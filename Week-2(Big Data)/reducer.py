def reducer(partitioned_data):
    result = {}

    for key, values in partitioned_data.items():
        # Sum all values for each genre
        result[key] = sum(values)

    return result