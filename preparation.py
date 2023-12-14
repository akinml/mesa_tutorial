###
### this can be packed in functions, for now I use the exported DataFrame
###
### lu.csv ###
# Upload a DataFrame of cantons, cities, longitude and latitude
canton_capitals = pd.read_csv("lu.csv")
canton_capitals = canton_capitals.copy()
# Mapping from city to lat and lon
city_to_lat = canton_capitals.set_index('city')['lat'].to_dict()
city_to_lon = canton_capitals.set_index('city')['lng'].to_dict()
# Map lat and lon to each admin_name based on city
canton_capitals['admin_lat'] = canton_capitals['admin_name'].map(city_to_lat)
canton_capitals['admin_lon'] = canton_capitals['admin_name'].map(city_to_lon)
# fix one error (NA for Redange because of difference in writing)
# Find the lat and Lon for "Redange-sur-Attert"
redange_lat = canton_capitals.loc[canton_capitals['city'] == 'Redange-sur-Attert', 'lat'].iloc[0]
redange_lon = canton_capitals.loc[canton_capitals['city'] == 'Redange-sur-Attert', 'lng'].iloc[0]
# Update the lat and Lon for "Redange"
canton_capitals.loc[canton_capitals['admin_name'] == 'Redange', 'admin_lat'] = redange_lat
canton_capitals.loc[canton_capitals['admin_name'] == 'Redange', 'admin_lon'] = redange_lon
# Fix the name so that it corresponds to the canton name
canton_capitals['admin_name'] = canton_capitals['admin_name'].str.replace('-sur-Alzette', '')

### synthetic-lux-pop-dataset-100000.csv ###
# Upload the synthetic data for Luxembourg
df = pd.read_csv("synthetic-lux-pop-dataset-100000.csv")
df = df.copy()
# dropping useless
data = df.drop(["Date_of_birth", "Social_matricule", "hair_color", "hair_lenght", "First_name", "Unnamed: 0"], axis=1)
# Fix the name so that it corresponds to the name in the "lu.csv"
data['admin_name'] = data["Canton"].str.replace('Canton ', '')
# Merge the DataFrames on 'admin_name'
data = data.merge(canton_capitals[['admin_name', 'admin_lat', 'admin_lon']], on='admin_name', how='left')
# Export data
data.to_csv('exported.csv', index=False)
