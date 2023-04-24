import joblib
from django.shortcuts import render
import pandas as pd


def index(request):
    if request.method == 'POST':
        try:
            # avg_temp = float(request.POST.get('avg_temp'))
            soil_ph = float(request.POST.get('soil_ph'))
            # season = request.POST.get('season')
            soil_texture = request.POST.get('soil_texture')
            sowing_month = request.POST.get('sowing_month')
            place = request.POST.get('place')
            place_hold = place
            crop_type = request.POST.get('crop_type')

            # Load the dataset with the required information
            season_temp_data = pd.read_excel('temperature.xlsx')
            print(season_temp_data.head(2))

            # Get the average temperature and season based on the user's inputs of sowing_month and place
            avg_temp = season_temp_data.loc[(season_temp_data['place'] == place) & (
                season_temp_data['sowing_month'] == sowing_month), 'avg_temp'].iloc[0]
            season = season_temp_data.loc[(season_temp_data['place'] == place) & (
                season_temp_data['sowing_month'] == sowing_month), 'season'].iloc[0]

            print(avg_temp, season)

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
            print(crop_pred)
            crop_data = pd.read_excel("crop_details.xlsx")
            yield_pred = crop_data.loc[(crop_data['Crop'] == crop_pred) & (
                crop_data['Place'] == place_hold), 'Yield'].iloc[0]
            price_pred = crop_data.loc[(crop_data['Crop'] == crop_pred) & (
                crop_data['Place'] == place_hold), 'Price'].iloc[0]

            # print(yield_pred)
            # print(price_pred)
            # Render the output template with the crop prediction and retrieved crop data
            return render(request, 'output.html', {'crop_pred': crop_pred, 'place': place_hold, 'yield_pred': yield_pred, 'price_pred': price_pred})

        except:
            return render(request, 'index.html', {'error_msg': 'No crops for given input'})

    else:
        return render(request, 'index.html')
