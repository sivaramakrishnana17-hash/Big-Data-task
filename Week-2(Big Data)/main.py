from mapper import mapper
from partitioner import partition
from reducer import reducer


def main():
    # Read input file
    with open("input.txt", "r") as file:
        data = file.readlines()

    # Step 1: Map
    mapped_data = mapper(data)

    # Step 2: Partition
    partitioned_data = partition(mapped_data)

    # Step 3: Reduce
    result = reducer(partitioned_data)

    # Display final output
    print("Final MapReduce Result")
    print("----------------------")

    for genre, count in result.items():
        print(f"{genre}: {count}")


if __name__ == "__main__":
    main()