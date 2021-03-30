import streamlit as st
import gzip 
import dill 
import pandas as pd 

area_dict = {"yaba": 7,"ajah": 0,"gbagada": 1,"surulere": 6,"ikeja": 2,"lekki": 5,"ikorodu": 3,"ikoyi": 4,}
propertytype_dict = {"Flat / apartment": 3, "Mini flat": 5, "Self contain": 7, 
        "Blocks of flats": 0, "Terraced duplex": 11, "Semi detached duplex": 9, "Detached duplex": 2,
         "Penthouse flat": 6, "Detached bungalow":1, "Massionette house":4,
          "Semi detached bungalow":8, "Terraced bungalow":10  }
def analysis(bed, bath, toilet, propertytype, area, parkingspace,
 security, electricity, furnished, securitydoors, cctv, bq, gym, pool):
    d_dict = {"Yes": 1, "No": 0}
    data = pd.DataFrame({ 'Bed': [bed], 'Bath': [bath], 'Toilet': [toilet], 'Property Type': [propertytype_dict[propertytype]], 'Area': [area_dict[area]],
       'Parking Space': [d_dict[parkingspace]], 'Security': [d_dict[security]], 'Electricity':[d_dict[electricity]], 'Furnished': [d_dict[furnished]],
       'Security Doors': [d_dict[securitydoors]] , 'CCTV': [d_dict[cctv]], 'BQ':[d_dict[bq]], 'Gym': [d_dict[gym]], 'Pool':[d_dict[pool]]})
    with gzip.open('model.dill.gzip', 'rb') as f:
        model = dill.load(f)
   # print(data)
    prediction = (model.predict(data)[0]).round(-3)  
    return prediction


def main():
    st.image('gradientboost.png')
    st.title('Lagos state House Predictor')
    st.subheader('An application to give you an estimate of price for renting houses in selected locations in Lagos.')
    new = st.sidebar.selectbox("Would you want details on the model and the data used or see it in Action", ["Model and Data Description", "Model in Action"])
    if new == "Model and Data Description":
        st.subheader("This Dashboard would help you understand how this model works and data used")
        st.markdown("To run our model please choose model in Action in the sidebar")
    
        st.markdown("If you are interested in finding out more about this model click the select box below\n it tells you more about the model or how the data was gotten")
        st.markdown("\nIf you want to know more about our model performance, \nselect what you would want to know")
        sel = st.radio("Please select what you would like to know", ["None","More about the data", "Model used and accuracy"])
        if sel == "More about the data":
            st.markdown("This data was gotten from PropertyProNG we used requests-html library to scrap the data")
        if sel == "Model used and accuracy":
            st.markdown("The model used for this was catboost Regressor")

    if new == "Model in Action":
        st.title("House rent price prediction model for selected locations in Lagos")
        st.markdown("Please select the location you want to rent an house")
        area = st.selectbox("Your preferred location", tuple(area_dict.keys()))
        st.markdown("Please select the kind of house you are interested in")
        propertytype = st.selectbox("Your preferred property type", tuple(propertytype_dict.keys()))
        st.markdown("Please enter the number of bedrooms you want from 1 to 10")
        bed = st.number_input("Input the number of bedrooms", min_value=1, max_value=10)
        st.markdown("Please enter the number of bathrooms you want from 1 to 10")
        bath = st.number_input("Input the number of bathrooms", min_value=1, max_value=10)
        st.markdown("Please enter the number of restroom you want from 1 to 10")
        toilet = st.number_input("Input the number of restrooms", min_value=1, max_value=10)
        st.markdown("Please select if you want 24/7 electricity or not")
        electricity =st.selectbox("Do you want 24/7 electricity?", ["Yes", "No"])
        st.markdown("Please select if you want a Boy quarters")
        bq = st.selectbox("Do you want a Boys Quarters?", ["Yes", "No"])
        st.markdown("Please select if you want a house that is already fully furnished ")
        furnished = st.selectbox("Do you want an house that is already furnished?", ["Yes", "No"])
        st.markdown("Please select if you want CCTV")
        cctv = st.selectbox("Do you want CCTV?", ["Yes", "No"])
        st.markdown("Please select if you want a GYM")
        gym = st.selectbox("Do you want a GYM?", ["Yes", "No"])
        st.markdown("Please select if you want a pool")
        pool = st.selectbox("Do you want a pool?", ["Yes", "No"])
        st.markdown("Please select if you want Security Guards")
        security = st.selectbox("Do you want assigned security guards?", ["Yes", "No"])
        st.markdown("Please select if you want Parking space")
        parkingspace = st.selectbox("Do you want an house with parking space?", ["Yes", "No"])
        st.markdown("Please select if you want a house with security doors")
        securitydoors = st.selectbox("Do you want an house with security doors?", ["Yes", "No"])
        
        result = analysis(bed, bath, toilet, propertytype, area, parkingspace,
            security, electricity, furnished, securitydoors, cctv, bq, gym, pool)
        
        if st.button('Check Price Estimate'):
            st.header(f'The estimated price of {propertytype} in {area}  is ₦ {result:,}')

#str(can you make edit?) 


if __name__ == "__main__":
    main()
