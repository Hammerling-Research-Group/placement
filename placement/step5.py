#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 10:22:07 2023

@author: mengjia
"""
import numpy as np
class PROSS:
    def __init__(self, matrix, k, min_detected_sensor,
                 recombination = 'onepoint', 
                 n_iters = None, patience = 100, check_steps = 1000,
                 seed = None, verbose = True):
        self.matrix = matrix
        self.n_rows = matrix.shape[0] # rows are sensor locations
        self.n_cols = matrix.shape[1] # columns are emission scenarios
        self.k = k
        self.min_detected_sensor = min_detected_sensor
        if n_iters == None:
            self.n_iters = round(self.n_rows * k * k * np.exp(1))
        else:
            self.n_iters = n_iters
        self.mut_prob = 1 / self.n_rows # mutation probability
        self.recombination = recombination
        self.opt_val_ub = np.sum(np.sum(matrix, axis=0) >= min_detected_sensor) # upper bound of the optimal value
        
        # initialize placeholders
        
        ## randomly select a row as the initial solution
        init_solution = np.zeros((1, self.n_rows))
        np.random.seed(seed)
        init_solution[0, np.random.randint(0, self.n_rows)] = 1
        np.random.seed(None)
        self.population = init_solution.reshape((1, -1))
        self.population_size = 1
        self.fitness_log = np.zeros((1, 2)) # first value = obj; second value = |solution|
        
        # best solution placeholder
        self.best_solution = init_solution
        self.best_opt_val = 0
        
        # other parameter
        self.patience = patience
        self.check_steps = check_steps
        self.verbose = verbose # suppress output or not
        
    
    def objectives(self, solution):
        submatrix = self.matrix[np.array(solution, dtype=bool)]
        obj_val1 = np.sum(np.sum(submatrix, axis=0) >= self.min_detected_sensor) # detection coverage
        obj_val2 = np.sum(solution) # solution size
        return [obj_val1, obj_val2]
    
    def recombination_onepoint(self, solution1, solution2):
        split_idx = np.random.randint(0, self.n_rows) 
        solution1_recomb = np.concatenate((solution1[:split_idx], solution2[split_idx:]))
        solution2_recomb = np.concatenate((solution2[:split_idx], solution1[split_idx:]))
        
        return solution1_recomb, solution2_recomb
    
    def recombination_uniform(self, solution1, solution2):
        a = np.random.choice([1, 0], size = self.n_rows, 
                             replace = True, p = [.5, .5])
        solution1_recomb = a * solution1 + (1-a) * solution2
        solution2_recomb = solution1 + solution2 - solution1_recomb
        
        return solution1_recomb, solution2_recomb
    
    def mutation(self, solution1, solution2):
        temp1 = np.random.choice([1, 0], size = self.n_rows, 
                                replace = True, p = [self.mut_prob, 1-self.mut_prob])
        solution1_mut = np.abs(solution1 - temp1)
        temp2 = np.random.choice([1, 0], size = self.n_rows, 
                                replace = True, p = [self.mut_prob, 1-self.mut_prob])
        solution2_mut = np.abs(solution2 - temp2)
        
        return solution1_mut, solution2_mut
    
    def find_best_solution(self):
        comb_matrix = np.hstack((self.fitness_log, self.population))
        val_comb_matrix = comb_matrix[comb_matrix[:, 1] <= self.k]
        val_comb_matrix_sorted = val_comb_matrix[np.argsort(val_comb_matrix[:,1])]
        best_row_id = np.argmax(val_comb_matrix_sorted[:, 0])
        
        best_row = val_comb_matrix_sorted[best_row_id]
        best_val = int(best_row[0])
        best_solution = best_row[2:]
        selected_row_ids = np.where(best_solution == 1)[0]
        return selected_row_ids, best_val
        
    
    def early_stop(self, items):
        '''
        Return True if all items are the same, return False otherwise.
        '''
        if len(set(items)) == 1:
            print('Early stop is reached!')
            return True
        else:
            return False
        
    
    def main(self):
        counter = 1
        best_solution_found = False
        early_stop = False
        fitness_monitor = [np.random.rand() for _ in range(self.patience)] # for early stop check
        while (counter < self.n_iters) & (best_solution_found == False) & (early_stop == False):
            # randomly select from population
            s1 = self.population[np.random.randint(self.population_size), :] # randomly select an existing solution 1
            s2 = self.population[np.random.randint(self.population_size), :] # randomly select an existing solution 2
            
            # recombination
            if self.recombination == 'onepoint':
                s1, s2 = self.recombination_onepoint(s1, s2)
            elif self.recombination == 'uniform':
                s1, s2 = self.recombination_uniform(s1, s2)
            else:
                raise ValueError("The input recombination approach is not implemented. Choose from 'onepoint' and 'uniform'. ")
                
            
            # bit-wise mutation
            s1, s2 = self.mutation(s1, s2)
            
            
            # check dominance
            for q in [s1, s2]:
                fitness = self.objectives(q)
                if 0 < fitness[1] < 2 * self.k:
                    
                    # compute dominance condition
                    condition = (self.fitness_log[:, 0] > fitness[0]) & (self.fitness_log[:, 1] <= fitness[1])
                    condition |= (self.fitness_log[:, 0] >= fitness[0]) & (self.fitness_log[:, 1] < fitness[1])
                    
                    if not np.any(condition):
                        # delete solutions worse than q
                        del_indx = (self.fitness_log[:, 0] <= fitness[0]) & (self.fitness_log[:, 1] >= fitness[1])
                        
                        # update population
                        self.population = np.vstack((self.population[~del_indx], q))
                        self.population_size = self.population.shape[0]
                        
                        # update fitness log
                        self.fitness_log = np.vstack((self.fitness_log[~del_indx], fitness))
            
            counter += 1 
            
            # check current best solution periodically
            
            if counter % (1000) == 0: # or use self.k * self.n_rows
                current_best_solution, current_best_val = self.find_best_solution()
                self.best_solution = current_best_solution
                self.best_opt_val = current_best_val
                
                # update the monitoring list by FIFO
                fitness_monitor.append(current_best_val)
                fitness_monitor.pop(0)
                
                # check early stop
                early_stop = self.early_stop(fitness_monitor)
                
                if self.verbose:
                    print('Iteration #{}: current best model: {} out of {} scenarios are detected'.format(counter, current_best_val, self.n_cols))
                if current_best_val == self.opt_val_ub:
                    best_solution_found = True
            
        # return the best solution after iterations
        best_solution, best_val = self.find_best_solution()
        self.best_solution = current_best_solution
        self.best_opt_val = current_best_val
        
        return best_solution, best_val
