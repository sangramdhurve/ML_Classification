import os
import pathlib

base_dir = pathlib.Path(__file__).parent.absolute().parent
data_dir = os.path.join(base_dir, "data")
logs_dir = os.path.join(base_dir, "logs")

if os.path.exists(logs_dir) is False:
    os.mkdir(logs_dir)

options = dict()
options["log_path"] = logs_dir
options["models_dir"] = os.path.join(data_dir, "models")

options["model_to_use"] = "LogisticRegressionModel"  # name of the class of the model
options["lead_score_model_path"] = os.path.join(options["models_dir"], "lead_score_model.pkl")

options["numerical_cols"] = ['total_visits', 'total_time_spent_on_website', 'page_views_per_visit']

# categorical cols that are used by the model and their respective unique values
options["categorical_cols"] = {'lead_source': ['Click2call', 'Pay per Click Ads', 'google'],
                               'last_activity': ['Email Received', 'Had a Phone Conversation'],
                               'specialization': ['Media and Advertising', 'Services Excellence'],
                               'search': ['Yes'],
                               'newspaper': ['No', 'Yes'],
                               'last_notable_activity': ['Unreachable']}

# all the categorical cols needed by the model and their corresponding unique values, including the values that are
# not needed by the model. this is used for input validation

options["categorical_cols_and_all_unique_values"] = {
    'lead_source': ['Click2call',
                    'Direct Traffic',
                    'Facebook',
                    'Live Chat',
                    'NC_EDM',
                    'Olark Chat',
                    'Organic Search',
                    'Pay per Click Ads',
                    'Press_Release',
                    'Reference',
                    'Referral Sites',
                    'Social Media',
                    'WeLearn',
                    'Welingak Website',
                    'bing',
                    'blog',
                    'google',
                    'testone',
                    'welearnblog_Home',
                    'youtubechannel'],

    'last_activity': ['Approached upfront',
                      'Converted to Lead',
                      'Email Bounced',
                      'Email Link Clicked',
                      'Email Marked Spam',
                      'Email Opened',
                      'Email Received',
                      'Form Submitted on Website',
                      'Had a Phone Conversation',
                      'Olark Chat Conversation',
                      'Page Visited on Website',
                      'SMS Sent',
                      'Unreachable',
                      'Unsubscribed',
                      'View in browser link Clicked',
                      'Visited Booth in Tradeshow'],

    'specialization': ['Banking, Investment And Insurance',
                       'Business Administration',
                       'E-Business',
                       'E-COMMERCE',
                       'Finance Management',
                       'Healthcare Management',
                       'Hospitality Management',
                       'Human Resource Management',
                       'IT Projects Management',
                       'International Business',
                       'Marketing Management',
                       'Media and Advertising',
                       'Operations Management',
                       'Retail Management',
                       'Rural and Agribusiness',
                       'Select',
                       'Services Excellence',
                       'Supply Chain Management',
                       'Travel and Tourism'],
    'search': ['Yes', 'No'],
    'newspaper': ['No', 'Yes'],

    'last_notable_activity': ['Approached upfront',
                              'Email Bounced',
                              'Email Link Clicked',
                              'Email Marked Spam',
                              'Email Opened',
                              'Email Received',
                              'Form Submitted on Website',
                              'Had a Phone Conversation',
                              'Modified',
                              'Olark Chat Conversation',
                              'Page Visited on Website',
                              'SMS Sent',
                              'Unreachable',
                              'Unsubscribed',
                              'View in browser link Clicked']
}

# please do not change the order of the columns
options["all_cols_reqd_by_model"] = ['total_visits',
                                     'total_time_spent_on_website',
                                     'page_views_per_visit',
                                     'lead_source_Click2call',
                                     'lead_source_Pay per Click Ads',
                                     'lead_source_google',
                                     'last_activity_Email Received',
                                     'last_activity_Had a Phone Conversation',
                                     'specialization_Media and Advertising',
                                     'specialization_Services Excellence',
                                     'search_Yes',
                                     'newspaper_No',
                                     'newspaper_Yes',
                                     'last_notable_activity_Unreachable']

options["api_host"] = "0.0.0.0"
options["api_port"] = 5000
options["api_workers"] = 2
