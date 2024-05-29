import numpy as np

def transpose_last_first(arr):
  """
    This function transposes the input array by reversing the order of the last and first elements.

    Parameters:
    arr (list or numpy array): The input array.

    Returns:
    list or numpy array: A new array containing the transposed version of the input array.

    The function iterates through the input array, starting from the last element and ending at the second last element. For each element, it appends the corresponding element from the input array to a new array. Finally, it returns the new array containing the transposed version of the input array.
    """
  trans_arr = []
  for i in range(-1, len(arr)-1):
    result = arr[i]
    trans_arr.append(result)
  return trans_arr

def get_arr_difference(arr):
  """
    This function calculates the difference between the original array and its transposed version.

    Parameters:
    arr (list or numpy array): The input array.

    Returns:
    list or numpy array: A new array containing the differences between the corresponding elements of the original and transposed arrays.

    The function first transposes the input array using the 'transpose_last_first' function, then calculates the difference between the original and transposed arrays, and finally returns the new array containing the differences.
    """
  trans_arr = transpose_last_first(arr)
  diff_arr = []
  for i in range(len(arr)):
    subtract = arr[i] - trans_arr[i]
    diff_arr.append(subtract)
  return diff_arr

def cost_function(diff_arr):
  """
    This function calculates the cost function for the given difference array.

    Parameters:
    diff_arr (list or numpy array): The input array containing the differences between the corresponding elements of the original and transposed arrays.

    Returns:
    float: A single value representing the sum of the squares of the differences in the input array.

    The function iterates through the input array, squares each difference, and accumulates the squared differences to calculate the cost function.
    """
  cost_value = 0
  for j in range(len(diff_arr)):
    val_sq = diff_arr[j]**2
    cost_value += val_sq 
  return cost_value

def insert_at_zero(arr,insert_value):
  """
    This function inserts a given value at the beginning of the input array.

    Parameters:
    arr (list or numpy array): The input array.
    insert_value (any): The value to be inserted at the beginning of the array.

    Returns:
    list or numpy array: A new array containing the inserted value at the beginning of the input array.

    The function uses the numpy.insert() function to insert the given value at the beginning of the input array and returns the modified array.
    """
  mod_arr = np.insert(arr, 0, insert_value)
  return mod_arr
