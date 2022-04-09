from data_storage import ResultsParameters


class ProcessData:

    def __init__(self, tab_name, results_parameters):
        self.tab_name = tab_name
        self.results_parameters = results_parameters
        print('process data')

    def store_inputs(self):
        print(f'store inputs, {self.tab_name}')

    def store_results(self):
        print(self.results_parameters)
        print('store results')

    def generate_results(self):
        print('generate results')

    def modify_result(self):
        print('modify results')

    def delete_result(self):
        print('delete results')

    def load_existing_result_set(self):
        print('load existing results')
