import joblib
from django.shortcuts import render
import pandas as pd
import numpy as np

import joblib
from django.shortcuts import render


from django.shortcuts import render
import pandas as pd

def index(request):
    if request.method == 'POST':
        try:
            avg_temp = float(request.POST.get('avg_temp'))
            soil_ph = float(request.POST.get('soil_ph'))
            season = request.POST.get('season')
            soil_texture = request.POST.get('soil_texture')
            sowing_month = request.POST.get('sowing_month')
            place = request.POST.get('place')
            place_hold=place
            crop_type = request.POST.get('crop_type')

            # Create a new dataframe with default values of 0
            new_data = pd.DataFrame({'soil_pH': [0], 'avg_temp': [0], 'baglung': [0], 'gorkha': [0],
                                     'lamjung': [0], 'syangja': [0], 'tanahu': [0], 'Sep/oct': [0],
                                     'june/july': [0], 'mar/apr': [0], 'oct/nov': [0],
                                     ' sandy clay loam': [0], 'clay': [0], 'clay loam': [0], 'loam': [0],
                                     'sandy loam': [0], 'silt': [0], 'silt loam': [0], 'summer': [0],
                                     'winter': [0], 'cereals': [0], 'other': [0]})

            # Update the dataframe with the user inputs
            new_data.loc[0, 'avg_temp'] = avg_temp
            new_data.loc[0, 'soil_pH'] = soil_ph
            new_data.loc[0, season] = 1
            new_data.loc[0, soil_texture] = 1
            new_data.loc[0, sowing_month] = 1
            new_data.loc[0, place] = 1
            new_data.loc[0, crop_type] = 1

            print(new_data)
            # Load the trained model and get crop recommendation
            model = pd.read_pickle('randomforest.pkl')
            crop_pred = model.predict(new_data)[0]
            #print(crop_pred)
            crop_data=pd.read_excel("crop_details.xlsx")
            yield_pred = crop_data.loc[(crop_data['Crop'] == crop_pred) & (crop_data['Place'] == place_hold), 'Yield'].iloc[0]
            price_pred = crop_data.loc[(crop_data['Crop'] == crop_pred) & (crop_data['Place'] == place_hold), 'Price'].iloc[0]

            # print(yield_pred)
            # print(price_pred)
            # Render the output template with the crop prediction and retrieved crop data
            return render(request, 'output.html', {'crop_pred': crop_pred,'place':place_hold, 'yield_pred': yield_pred, 'price_pred': price_pred})

        except:
            return render(request, 'index.html', {'error_msg': 'No crops for given input'})

    else:
        return render(request, 'index.html')



















# # Define a function to preprocess the input data
# def preprocess_input(data):
#     # One-hot encode the categorical features
#     season = pd.get_dummies(data['season'])
#     soil_texture = pd.get_dummies(data['soil_texture'])
#     sowing_month = pd.get_dummies(data['sowing_month'])
#     place = pd.get_dummies(data['place'])
#     crop_type = pd.get_dummies(data['crop_type'])
#     # Combine the one-hot encoded features with the numerical features
#     input_features = pd.concat([data['avg_temp'], data['soil_ph'], season, soil_texture, sowing_month, place,crop_type], axis=1)
#     print(input_features)
#     return input_features

# # Define the view function
# def crop_recommendation(request):
#     if request.method == 'POST':
#         # Preprocess the input data
#         input_data = {
#             'avg_temp': request.POST.get('avg_temp'),
#             'soil_ph': request.POST.get('soil_ph'),
#             'season': request.POST.get('season'),
#             'soil_texture': request.POST.get('soil_texture'),
#             'sowing_month': request.POST.get('sowing_month'),
#             'place': request.POST.get('place'),
#             'crop_type': request.POST.get('crop_type')
#                     # convert the selected option to 1 and all other options to 0
#         }
#         print(input_data)
#         input_features = preprocess_input(pd.DataFrame(input_data, index=[0]))
#         print(input_features.columns)
#         # Use the pre-trained model to predict the crop
#         crop_pred = rf_model.predict(input_features)[0]
#         crop_pred = le_crop.inverse_transform([crop_pred])[0]
#         # Render the result page
#         return render(request, 'result.html', {'crop_pred': crop_pred})
#     else:
#         # Render the input form page
#         return render(request, 'index.html')


# import pandas as pd
# import joblib
# from django.shortcuts import render

# def crop_recommendation(request):
#     if request.method == 'POST':
#         avg_temp = float(request.POST['avg_temp'])
#         soil_ph = float(request.POST['soil_ph'])
#         season = request.POST['season']
#         soil_texture = request.POST['soil_texture']
#         sowing_month = request.POST['sowing_month']
#         place = request.POST['place']
#         crop_type = request.POST['crop_type']

#         # Load the saved model
#         model = joblib.load('randomforest.pkl')



#         # Preprocess the input data
#         input_data = {'avg_temp': avg_temp, 'soil_ph': soil_ph, 'season': season,
#                       'soil_texture': soil_texture, 'sowing_month': sowing_month,
#                       'place': place, 'crop_type': crop_type}
        
#         input_data = pd.DataFrame([input_data])
#         input_data = input_data.join(pd.get_dummies(input_data['place']))
#         input_data = input_data.join(pd.get_dummies(input_data['soil_texture']))
#         input_data = input_data.join(pd.get_dummies(input_data['season']))
#         input_data = input_data.join(pd.get_dummies(input_data['sowing_month']))
#         input_data = input_data.join(pd.get_dummies(input_data['crop_type']))
#         print("input")
#         print(input_data)
#         input_data = input_data.drop('place', axis=1)
#         input_data = input_data.drop('season',axis=1)
#         input_data = input_data.drop('soil_texture',axis=1)
#         input_data = input_data.drop('sowing_month',axis=1)
#         input_data = input_data.drop('crop_type',axis=1)
#         # input_df = pd.DataFrame([input_data])
#         # print(input_df)
#         # # One-hot encode the categorical features
#         # categorical_cols = ['season', 'soil_texture', 'sowing_month', 'place', 'crop_type']
#         # input_df = pd.get_dummies(input_df)
#         # print(input_df)

#         print(input_data)

#         # Drop the original categorical columns
#         # input_df = input_df.drop(columns=categorical_cols)



#         # # Get the prediction
#         # X = input_data.values.reshape(1, -1)
#         y_pred = model.predict(input_data)

#         # Show the prediction result on the result.html template
#         context = {'crop_pred': y_pred}
#         return render(request, 'result.html', context)

#     return render(request, 'index.html')






#         #season
# #         if input_df['summer']== 1:
# #             input_df['winter']=0

        
# #         # if season=='winter':
# #         #     input_df['winter']=1
# #         # else:
# #         #     input_df['winter']=0


# #         #soil_texture
# #         if soil_texture=='clay':
# #             input_df['clay']=1
# #         else:
# #             input_df['clay']=0

        
# #         if soil_texture=='clay loam':
# #             input_df['clay loam']=1
# #         else:
# #             input_df['clay loam']=0

# #         if soil_texture=='sandy clay loam':
# #             input_df['sandy clay loam']=1
# #         else:
# #             input_df['sandy clay loam']=0

        
# #         if soil_texture=='loam':
# #             input_df['loam']=1
# #         else:
# #             input_df['loam']=0

# #         if soil_texture=='sandy loam':
# #             input_df['sandy loam']=1
# #         else:
# #             input_df['sandy loam']=0

        
# #         if soil_texture=='silt loam':
# #             input_df['silt loam']=1
# #         else:
# #             input_df['silt loam']=0

# #         if soil_texture=='silt':
# #             input_df['silt']=1
# #         else:
# #             input_df['silt']=0


# # #sowing_month
        
# #         if sowing_month=='mar/apr':
# #             input_df['mar/apr']=1
# #         else:
# #             input_df['mar/apr']=0

# #         if sowing_month=='june/july':
# #             input_df['june/july']=1
# #         else:
# #             input_df['june/july']=0

        
# #         if sowing_month=='Sep/oct':
# #             input_df['Sep/oct']=1
# #         else:
# #             input_df['Sep/oct']=0

# #         if sowing_month=='oct/nov':
# #             input_df['oct/nov']=1
# #         else:
# #             input_df['oct/nov']=0

# # #place
# #         if place=='baglung':
# #             input_df['baglung']=1
# #         else:
# #             input_df['baglung']=0

# #         if place=='gorkha':
# #             input_df['gorkha']=1
# #         else:
# #             input_df['gorkha']=0

        
# #         if place=='lamjung':
# #             input_df['lamjung']=1
# #         else:
# #             input_df['lamjung']=0

# #         if place=='tanahu':
# #             input_df['tanahu']=1
# #         else:
# #             input_df['tanahu']=0

        
# #         if place=='syangja':
# #             input_df['syangja']=1
# #         else:
# #             input_df['syangja']=0


# # #crop_type


# #         if crop_type=='cereals':
# #             input_df['cereals']=1
# #         else:
# #             input_df['cereals']=0

        
# #         if crop_type=='other':
# #             input_df['other']=1
# #         else:
# #             input_df['other']=0

# #         print(input_df)