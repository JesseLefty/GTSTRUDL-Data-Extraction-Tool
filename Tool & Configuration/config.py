load_file_types = [('*.gto - GTSTRUDL Output', '*.gto'), ('*.txt - Text Files', '*.txt')]
store_file_types = [('*.prop - properties file', '*.prop')]
output_file_types = [('*.xlsx - Microsoft Excel', '*.xlsx'), ('*.csv - Comma Separated Value (csv)', '*.csv')]
available_results_headings = ['Set #', 'Set Name', 'Input line #']
text_box_color_disable = 'grey95'
text_box_color_enable = 'white'
codes = ['AISC14', 'N690-12', '341-10', 'N690-94', 'AISC13', 'N690-06', 'LRFD3', 'ASD9-E', 'LRFD-2', 'ASD9', '78AISC',
         '69AISC', 'W78AISC', 'DBLANG', 'W69AISC']

rb_options = {1: '',
              2: 'Starts With: ',
              3: 'Ends With: ',
              4: 'Contains: ',
              5: 'List: '}

requested_results_headings = {'Member Force':
                                  {'headings': ['Set #', 'Set Name', 'Joint Spec.', 'Name Spec.', 'Load Spec.'],
                                   'column width': [40, 180, 95, 95, 95],
                                   'text location': ['center', 'w', 'center', 'w', 'w'],
                                   'text label': ['MEMBER NAME(s)', 'LOAD CASE(s)', 'JOINT(s)']},
                              'Joint Reaction':
                                  {'headings': ['Set #', 'Set Name', 'Name Spec.', 'Load Spec.'],
                                   'column width': [40, 300, 100, 100],
                                   'text location': ['center', 'w', 'center', 'w'],
                                   'text label': ['JOINT NAME(s)', 'LOAD CASE(s)']},
                              'Code Check':
                                  {'headings': ['Set #', 'Set Name', 'Name Spec.', 'Profile Spec.', 'IR Range', 'Sort'],
                                   'column width': [40, 200, 95, 95, 65, 45],
                                   'text location': ['center', 'w', 'center', 'w', 'w', 'w'],
                                   'text label': ['MEMBER NAME(s)', 'PROFILE(s)', 'IR RANGE']}
                              }

result_configuration_parameters = {'Member Force':
                                       {'Trigger String': 'LIST FOR',
                                        'Skip Lines': 22,
                                        'End Trigger': '1',
                                        'Headings': ['MEMBER', 'LOAD', 'JOINT', 'FOR X', 'FOR Y', 'FOR Z', 'MOM X',
                                                     'MOM Y', 'MOM Z']},
                                   'Joint Reaction':
                                       {'Trigger String': 'RESULTANT JOINT LOADS SUPPORTS',
                                        'Skip Lines': 3,
                                        'End Trigger': '1',
                                        'Headings': ['JOINT', 'LOAD', 'FOR X', 'FOR Y', 'FOR Z', 'MOM X', 'MOM Y',
                                                     'MOM Z']},
                                   'Code Check':
                                       {'Trigger String': 'DESIGN TRACE OUTPUT',
                                        'Skip Lines': 13,
                                        'End Trigger': 'END OF TRACE OUTPUT',
                                        'Headings': ['MEMBER', 'TABLE', 'LOAD CASE', 'SECTION LOCATION',
                                                     'STRESS PROVISION', 'STRESS IR', 'CODE', 'PROFILE',
                                                     'SHAPE PROVISION', 'GEOMETRY IR', 'FOR X', 'FOR Y', 'FOR Z',
                                                     'MOM X', 'MOM Y', 'MOM Z', 'UNITS', 'PASS/FAIL']}
                                   }
