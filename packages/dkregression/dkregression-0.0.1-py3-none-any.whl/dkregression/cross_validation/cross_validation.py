import torch
from ..likelihoods import log_likelihood

class CrossValidation():
    def __init__(self,max_evaluations=100,max_data_withhold=0.1) -> None:
        self.max_evaluations = max_evaluations   #how many times the log_likelihood function should be called at max
        self.max_data_withhold = max_data_withhold   #what is the maximum percentage of data points to be removed from the training dataset and withheld for testing

    def split_data(self,x_raw,y_raw):
        # output is a list of dictionaries with the keys: 'x', 'y', 'y', and 'yq'
        n = x_raw.shape[0]
        total_max_data_withhold = int(n*self.max_data_withhold*self.max_evaluations)

        # case 1: max_evaluations >= n (leave-one-out cross validation possible)
        if self.max_evaluations >= n:
            dataset = []
            for i in range(n):
                xq = x_raw[[i]]
                yq = y_raw[[i]]
                
                other_indices = torch.ones((n,),dtype=torch.bool)
                other_indices[i] = False

                x = x_raw[[other_indices]]
                y = y_raw[[other_indices]]

                dataset.append({'x':x, 'y':y, 'xq':xq, 'yq':yq})

            return dataset

        
        # case 2: total_max_data_withhold >= n (full cross validation is possible)
        # In this case, we will try to max out the number of evaluations to keep the number of samples per trial as small as possible
        if total_max_data_withhold >= n:
            rand_idx = torch.randperm(n)
            split = torch.tensor_split(rand_idx,self.max_evaluations)
            dataset = []
            for s in split:
                xq = x_raw[[s]]
                yq = y_raw[[s]]
                
                other_indices = torch.ones((n,),dtype=torch.bool)
                other_indices[[s]] = False

                x = x_raw[[other_indices]]
                y = y_raw[[other_indices]]

                dataset.append({'x':x, 'y':y, 'xq':xq, 'yq':yq})

            return dataset


        # case 3: total_max_data_withhold < n (withheld samples are randomly selected)
        # In this case, we will always select max_data_withhold samples
        if total_max_data_withhold < n:
            rand_idx = torch.randperm(n)[:total_max_data_withhold]
            split = torch.tensor_split(rand_idx,self.max_evaluations)
            dataset = []
            for s in split:
                xq = x_raw[[s]]
                yq = y_raw[[s]]
                
                other_indices = torch.ones((n,),dtype=torch.bool)
                other_indices[[s]] = False

                x = x_raw[[other_indices]]
                y = y_raw[[other_indices]]

                dataset.append({'x':x, 'y':y, 'xq':xq, 'yq':yq})

            return dataset
    
    def evaluate_likelihood(self,dataset,kernel,likelihood):
        log_probs = []
        for d in dataset:
            log_probs.append(log_likelihood(d['x'],d['y'],d['xq'],d['yq'],kernel,likelihood))

        return torch.mean(torch.Tensor(log_probs))
