file_types = [('*.prop - properties file', '*.prop')]
available_results_headings = ['Set #', 'Set Name', 'Input line #']

rb_options = {1: '',
              2: 'Starts With: ',
              3: 'Ends With: ',
              4: 'Contains: ',
              5: 'List: '}


requested_results_headings = {'Member Force':
                                  {'headings': ['Set #', 'Set Name', 'Joint Spec.', 'Name Spec.', 'Load Spec.'],
                                   'column width': [40, 200, 100, 100, 100],
                                   'text location': ['center', 'w', 'center', 'w', 'w'],
                                   'text label': ['MEMBER NAME(s)', 'LOAD CASE(s)', 'JOINT(s)']},
                              'Joint Reaction':
                                  {'headings': ['Set #', 'Set Name', 'Name Spec.', 'Load Spec.'],
                                   'column width': [40, 200, 100, 100],
                                   'text location': ['center', 'w', 'center', 'w'],
                                   'text label': ['JOINT NAME(s)', 'LOAD CASE(s)']},
                              'Code Check':
                                  {'headings': ['Set #', 'Set Name', 'Name Spec.', 'Profile Spec.', 'IR Range', 'Sort'],
                                   'column width': [40, 150, 50, 50, 50, 50],
                                   'text location': ['center', 'w', 'center', 'w', 'w', 'w'],
                                   'text label': ['MEMBER NAME(s)', 'PROFILE(s)', 'IR RANGE']}
                              }
