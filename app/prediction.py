import random

class BloomFilter:
    def __init__(self, size, hash_count):
        """
        Initializes the Bloom Filter with a given size and number of hash functions.
        
        Parameters:
        - size: The number of bits in the bit array.
        - hash_count: The number of hash functions used.
        """
        self.size = size  # Total number of bits in the bit array
        self.hash_count = hash_count  # Number of hash functions
        self.bit_array = [0] * size  # A list initialized with zeros to represent the bit array

    def _hashes(self, item):
        """
        Generates multiple hash values for a given item.
        
        Parameters:
        - item: The item to be hashed.

        Returns:
        - A list of hash values.
        
        Example:
        If size = 10 and hash_count = 3, then for item 'apple':
        Hashes might be: [5, 6, 7] (values depend on the hash function).
        """
        hash_values = []
        base_hash = hash(item)  # Get the base hash of the item
        for i in range(self.hash_count):  # Generate hash_count number of hash values
            hash_value = (base_hash + i) % self.size  # Create a hash value within the range of bit array
            hash_values.append(hash_value)
        return hash_values

    def add(self, item):
        """
        Adds an item to the Bloom Filter by setting the relevant bits in the bit array.
        
        Parameters:
        - item: The item to be added.
        
        Example:
        For item 'apple', and if its hashes are [5, 6, 7], the bits at indices 5, 6, and 7 will be set to 1.
        """
        hash_values = self._hashes(item)  # Get the hash values for the item
        for hash_val in hash_values:  # Loop through each hash value
            self.bit_array[hash_val] = 1  # Set the corresponding bit to 1

    def check(self, item):
        """
        Checks if an item might be present in the Bloom Filter.
        
        Parameters:
        - item: The item to be checked.

        Returns:
        - True if the item might be present (all corresponding bits are 1).
        - False if the item is definitely not present (any corresponding bit is 0).
        
        Example:
        If item 'apple' has hashes [5, 6, 7], and all these bits in the array are 1, it returns True.
        If any of these bits is 0, it returns False.
        """
        hash_values = self._hashes(item)  # Get the hash values for the item
        for hash_val in hash_values:  # Check each corresponding bit
            if self.bit_array[hash_val] == 0:  # If any bit is not set, the item is definitely not present
                return False
        return True  # If all bits are set, the item might be present

class CountMinSketch:
    def __init__(self, width, depth):
        """
        Initialize the Count-Min Sketch table with given width and depth.
        - width: Number of columns in the table (affects accuracy).
        - depth: Number of rows in the table (affects probability of correctness).
        """
        self.width = width
        self.depth = depth
        # Create a 2D list to store counts, initialized to 0.
        self.table = []
        for _ in range(depth):
            self.table.append([0] * width)

        # Generate unique seeds for hash functions.
        self.seeds = []
        for _ in range(depth):
            self.seeds.append(random.randint(0, 1000))

    def _hash(self, item, seed):
        """
        Compute a hash value for the given item using a seed.
        - item: The object to hash.
        - seed: A unique value to vary the hash for each row.
        """
        hashed_value = hash(item)
        return (hashed_value + seed) % self.width

    def add(self, item):
        """
        Add an item to the Count-Min Sketch by updating counts in all rows.
        - item: The object to add.
        """
        for row in range(self.depth):
            index = self._hash(item, self.seeds[row])  # Calculate index for this row.
            self.table[row][index] += 1  # Increment the count at the computed index.

    def count(self, item):
        """
        Estimate the count of an item by finding the minimum count across all rows.
        - item: The object to check the frequency of.
        """
        counts = []
        for row in range(self.depth):
            index = self._hash(item, self.seeds[row])  # Calculate index for this row.
            counts.append(self.table[row][index])  # Retrieve the count at the computed index.
        return min(counts)  # Return the smallest count as the estimate.
