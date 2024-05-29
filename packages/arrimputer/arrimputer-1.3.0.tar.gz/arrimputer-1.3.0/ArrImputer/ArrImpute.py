import numpy as np
from numpy import random
from .utils import *

def get_optimum_integer(arr,specify_integer = None,max_tries=None):
  """
    This function finds the optimal integer to insert into the given array 'arr'
    such that the cost function is minimized. The cost function is not explicitly
    defined in this function, but it is assumed to be defined elsewhere.

    Parameters:
    arr (list): The input array where the integer will be inserted.
    specify_integer (int, optional): The integer to be inserted into the array.If not provided, a random integer will be chosen.
    max_tries (int, optional): The maximum number of attempts to find the optimal integer.
    If not provided, a default value of 20 will be used.

    Returns:
    bool: Returns True if the cost function is minimized, and False otherwise.

    Raises:
    ValueError: If 'max_tries' is not a positive integer.

    Example:
    >>> arr = [1, 2, 3, 4, 5]
    >>> get_optimum_integer(arr)
    cost_function is reduced to: 1.0 ; improvement percent: 100.0 ; insert value from single trial is: 1 ; index of insertion is: 0 1 ; # of iterations: 1
    """
  
  if max_tries == None:
    print(f'it is advisable to set max_tries to a value less than 1000')
    max_tries = 1000
  else:
    max_tries = max_tries

  if specify_integer is not None:
    test_integer = specify_integer
  else:
    test_integer = random.randint(0,2) #10**5

  reset_arr = arr
  reset_mod_arr = insert_at_zero(arr,test_integer)
  tarr = transpose_last_first(arr=arr)
  diff_arr = get_arr_difference(arr=arr)
  initial_cost = cost_function(diff_arr=diff_arr); print('previous cost function was:', initial_cost)
  position=0
  cost_minimized = False #assume no minimization de novo
  while_loop_counter=0
  
  while not cost_minimized and while_loop_counter < max_tries:
    for i in range(len(reset_arr)+1): 
      new_position = i
      position = new_position
      mod_arr = np.insert(arr,position,test_integer)
      arr = mod_arr

      if i < len(reset_arr):
        mod_tarr = np.insert(tarr,position+1,test_integer)
        tarr = mod_tarr
      elif i > len(reset_arr):
        mod_tarr = np.insert(tarr,position-1,test_integer)
        tarr = mod_tarr
        test_integer = new_test_integer

      diff_arr_new = []
      for j in range(len(tarr)):
        subtract = arr[j] - tarr[j]
        diff_arr_new.append(subtract)
        diff_arr = diff_arr_new

      new_cost = cost_function(diff_arr=diff_arr)
      if (new_cost - initial_cost) < 0:
        cost_minimized = True
        initial_cost = new_cost
        print('cost_function is reduced to:', new_cost ,' ; improvement percent:', round(((new_cost - initial_cost) / initial_cost) * 100, 4), '; insert value from single trial is:',test_integer, '; index of insertion is:', position, position + 1, ' ; # of iterations:', while_loop_counter)
        return new_cost
      else:
        if i < len(reset_arr)-1:
          arr = np.delete(mod_arr,position,axis=0) 
          tarr = np.delete(mod_tarr,position+1,axis=0) 
        elif i == len(reset_arr)-1: 
          arr = reset_arr 
          tarr = reset_mod_arr
        elif i == len(reset_arr):
          arr = np.delete(mod_arr,position,axis=0) 
          tarr = np.delete(mod_tarr,position,axis=0) 
        
      print(initial_cost, new_cost, 'trying the next position(i+1): failed to minimize cost; position (arr, arr-1) =', i, i+1)
      while_loop_counter += 1

    if (new_cost - initial_cost) < 0:
      print('cost minimized:', new_cost, ' ; working integer:', test_integer, ' ; insert position(s) are:', position, position+1)
      return new_cost
    
    elif while_loop_counter > max_tries:
      print('Aborting...:Max tries exceeded so increase the range.', 'New cost: ', new_cost, 'Initial cost: ', initial_cost)
      return new_cost
      
    else:
      new_test_integer = test_integer + 1
      test_integer = new_test_integer

def getMinimumCostInt(arr, delta=1000):
  """
    This function finds the optimal integer to insert into the given array 'arr'
    such that the cost function is minimized. The cost function is not explicitly
    defined in this function, but it is assumed to be defined elsewhere.

    Parameters:
    arr (list): The input array where the integer will be inserted.
    delta (int, optional): The maximum number of attempts to find the optimal integer.
    If not provided, a default value of 1000 will be used.

    Returns:
    float: The minimum cost function value after inserting the optimal integer.

    Raises:
    ValueError: If 'delta' is not a positive integer.

    Example:
    >>> arr = [1, 2, 3, 4, 5]
    >>> getMinimumCostInt(arr)
    cost_function is reduced to: 1.0 ; improvement percent: 100.0 ; insert value from single trial is: 1 ; index of insertion is: 0 1 ; # of iterations: 1
    """
  insert_value = random.randint(0,2)
  reset_arr = arr
  n = len(reset_arr)
  position = 0
  int_iter = 0
  
  arr_rs = []
  for i in range(-1, len(arr)-1):
    result = arr[i]
    arr_rs.append(result)
  reset_mod_arr = np.insert(arr, 0, insert_value)
    
  sub_arr = []
  for j in range(len(arr_rs)):
    result_f = arr[j] - arr_rs[j]
    sub_arr.append(result_f)
      
  cost_function = 0
  for k in range(len(sub_arr)):
    val_sq = sub_arr[k]**2
    cost_function += val_sq 
  cost_function_old = cost_function
  print('previous cost function was:', cost_function)
  
  cost_minimized = False
  while not cost_minimized:
    for m in range(len(reset_arr)+1): 
      new_position = m 
      position = new_position
      
      new_arr = np.insert(arr, position, insert_value)
      arr = new_arr
      print(arr)
      
      if m < n:
        new_arr_rs = np.insert(arr_rs, position+1, insert_value)
        arr_rs = new_arr_rs
        print(arr_rs)
        
      elif m > n:
        new_arr_rs = np.insert(arr_rs, position-1, insert_value)
        arr_rs = new_arr_rs
        insert_value = new_insert_value
        print(arr_rs)
        
      sub_arr_new = []
      for l in range(len(arr_rs)):
        result_f_new = arr[l] - arr_rs[l]
        sub_arr_new.append(result_f_new)
        sub_arr = sub_arr_new
        print(sub_arr)
      
      new_cost_function = 0
      for k in range(len(sub_arr_new)):
        val_sq_new = sub_arr_new[k]**2
        new_cost_function += val_sq_new
      
      if (new_cost_function - cost_function) < 0:
        cost_minimized = True
        cost_function = new_cost_function 
        print('cost_function is reduced to:', new_cost_function ,' ; improvement percent:', round(((cost_function - cost_function_old) / cost_function_old) * 100, 4), '; insert value from single trial is:',insert_value, '; index of insertion is:', position, position + 1, ' ; # of iterations:', int_iter)
        return new_cost_function
      else:
        if m < n-1:
          arr = np.delete(new_arr,position,axis=0) 
          arr_rs = np.delete(new_arr_rs,position+1,axis=0) 
        elif m == n-1: 
          arr = reset_arr 
          arr_rs = reset_mod_arr
        elif m == n:
          arr = np.delete(new_arr,position,axis=0) 
          arr_rs = np.delete(new_arr_rs,position,axis=0) 
        
      print(cost_function, new_cost_function, 'trying the next position(m+1): failed to minimize cost; position (arr, arr-1) =', m, m+1)
      
      int_iter += 1
      
    if (new_cost_function - cost_function) < 0 or int_iter > delta :
      print('cost minimized or max tries exceeded:', new_cost_function, ' ; working integer:', insert_value, ' ; insert position(s) are:', position, position+1)
      return new_cost_function
    else:
      new_insert_value = insert_value + 1
      insert_value = new_insert_value
