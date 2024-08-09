#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
import mysql.connector

def fetch_data(query):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Saran@123",
        database="redbus_data_project"
    )
    cursor = con.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    cursor.close()
    con.close()
    return rows, column_names

with st.sidebar:
    state_transport_corp = st.selectbox('Select the State Transport Corporation:', 
    ['Rajasthan (RSRTC)', 'Kerala (KSRTC)', 'Himachal Pradesh (HRTC)', 'Punjab (PEPSU)', 'Bihar (BSRTC)', 
     'South Bengal (SBSTC)', 'West Bengal', 'Chandigarh (CTU)', 'Assam (ASTC)', 'Kadamba (KTCL)'])
    
    route_dict = {
        'Rajasthan (RSRTC)': ['Jodhpur to Ajmer', 'Beawar (Rajasthan) to Jaipur (Rajasthan)', 'Udaipur to Jodhpur', 
                               'Jaipur (Rajasthan) to Jodhpur', 'Sikar to Jaipur (Rajasthan)', 'Kishangarh to Jaipur (Rajasthan)', 
                               'Aligarh (uttar pradesh) to Jaipur (Rajasthan)', 'Jodhpur to Beawar (Rajasthan)', 
                               'Kota (Rajasthan) to Jaipur (Rajasthan)', 'Jaipur (Rajasthan) to Aligarh (uttar pradesh)', 
                               'Jaipur (Rajasthan) to Kota (Rajasthan)', 'Pali (Rajasthan) to Udaipur', 'Udaipur to Pali (Rajasthan)', 
                               'Sikar to Bikaner', 'Jaipur (Rajasthan) to Bharatpur', 'Kishangarh to Jodhpur', 
                               'Jaipur (Rajasthan) to Bhilwara', 'Kota (Rajasthan) to Udaipur', 'Jaipur (Rajasthan) to Pilani', 
                               'Jaipur (Rajasthan) to Mathura', 'Bikaner to Sikar'],
        'Kerala (KSRTC)': ['Bangalore to Kozhikode', 'Kozhikode to Ernakulam', 'Kozhikode to Bangalore', 
                            'Ernakulam to Kozhikode', 'Kozhikode to Mysore', 'Kozhikode to Thiruvananthapuram', 
                            'Bangalore to Kalpetta (kerala)', 'Mysore to Kozhikode', 'Kalpetta (kerala) to Bangalore', 
                            'Kozhikode to Thrissur', 'Thiruvananthapuram to Kozhikode', 'Bangalore to Kannur', 
                            'Kozhikode to Kottayam', 'Kannur to Bangalore', 'Kottayam to Kozhikode', 'Thrissur to Kozhikode', 
                            'Kozhikode to Kalpetta (kerala)', 'Coimbatore to Ooty', 'Kalpetta (kerala) to Kozhikode'],
        'Himachal Pradesh (HRTC)': ['Delhi to Shimla', 'Shimla to Delhi', 'Manali to Chandigarh', 'Chandigarh to Manali', 
                 'Delhi to Manali', 'Hamirpur (Himachal Pradesh) to Chandigarh', 'Delhi to Hamirpur (Himachal Pradesh)', 
                 'Delhi to Chandigarh', 'Manali to Delhi', 'Hamirpur (Himachal Pradesh) to Delhi', 
                 'Chandigarh to Hamirpur (Himachal Pradesh)', 'Shimla to Manali', 'Delhi to Dharamshala (Himachal Pradesh)', 
                 'Shimla to Chandigarh', 'Chandigarh to Dharamshala (Himachal Pradesh)', 'Delhi to Baddi (Himachal Pradesh)', 
                 'Dharamshala (Himachal Pradesh) to Chandigarh', 'Chamba (Himachal Pradesh) to Chandigarh', 
                 'Delhi to Dalhousie', 'Delhi to Chamba (Himachal Pradesh)', 'Dalhousie to Delhi', 'Solan to Delhi', 
                 'Delhi to Palampur', 'Dharamshala (Himachal Pradesh) to Delhi', 'Delhi to Solan', 
                 'Chandigarh to Reckong Peo (Himachal Pradesh)', 'Manali to Shimla', 'Palampur to Delhi', 
                 'Chandigarh to Kullu', 'Kangra to Chandigarh', 'Kullu to Chandigarh', 'Delhi to Kangra', 
                 'Chamba (Himachal Pradesh) to Delhi', 'Palampur to Chandigarh', 'Chandigarh to Shimla', 
                 'Chandigarh to Kangra', 'Delhi to Nalagarh', 'Baddi (Himachal Pradesh) to Delhi', 'Kangra to Delhi', 
                 'Ghumarwin to Delhi', 'Delhi to Sarkaghat'],
        'Punjab (PEPSU)': ['Patiala to Delhi', 'Delhi to Patiala', 'Ludhiana to Delhi', 'Delhi to Ludhiana', 
                 'Phagwara to Delhi', 'Jalandhar to Delhi', 'Delhi to Jalandhar', 'Patiala to Delhi Airport', 
                 'Jalandhar to Delhi Airport', 'Ludhiana to Delhi Airport', 'Phagwara to Delhi Airport', 
                 'Delhi Airport to Ludhiana', 'Delhi to Phagwara', 'Delhi to Amritsar', 'Amritsar to Delhi', 
                 'Delhi Airport to Patiala', 'Amritsar to Delhi Airport', 'Kapurthala to Delhi', 'Delhi Airport to Jalandhar', 
                 'Chandigarh to Bathinda', 'Chandigarh to Faridkot', 'Chandigarh to Patiala'],
        'Bihar (BSRTC)': ['Patna (Bihar) to Bettiah', 'Gopalganj (Bihar) to Delhi', 'Patna (Bihar) to Motihari', 
                 'Delhi to Motihari', 'Bettiah to Patna (Bihar)', 'Motihari to Delhi', 'Patna (Bihar) to Balmiki Nagar (bihar)', 
                 'Balmiki Nagar (bihar) to Patna (Bihar)', 'Patna (Bihar) to Kathmandu', 'Patna (Bihar) to Katihar', 
                 'Patna (Bihar) to Purnea', 'Patna (Bihar) to Hazaribagh', 'Ranchi to Patna (Bihar)', 
                 'Hazaribagh to Patna (Bihar)', 'Patna (Bihar) to Raxaul', 'Muzaffarpur (Bihar) to Kathmandu', 
                 'Patna (Bihar) to Ranchi', 'Muzaffarpur (Bihar) to Ranchi', 'Kathmandu to Patna (Bihar)', 
                 'Ranchi to Muzaffarpur (Bihar)', 'Motihari to Lucknow', 'Lucknow to Motihari', 'Motihari to Kathmandu', 
                 'Agra to Motihari', 'Patna (Bihar) to Janakpur (Nepal)', 'Muzaffarpur (Bihar) to Hazaribagh', 
                 'Purnea to Patna (Bihar)', 'Patna (Bihar) to Araria (Bihar)', 'Darbhanga to Patna (Bihar)', 
                 'Patna (Bihar) to Saharsa', 'Motihari to Agra', 'Hajipur (Bihar) to Kathmandu', 'Kathmandu to Motihari', 
                 'Patna (Bihar) to Forbesganj', 'Ranchi to Hajipur (Bihar)', 'Lucknow to Gopalganj (Bihar)'],
        'South Bengal (SBSTC)': ['Burdwan to Kolkata', 'Kolkata to Burdwan', 'Durgapur (West Bengal) to Kolkata', 
                 'Kolkata to Haldia', 'Haldia to Kolkata', 'Kolkata to Durgapur (West Bengal)', 
                 'Kolkata to Arambagh (West Bengal)', 'Digha to Kolkata', 'Kolkata to Digha', 'Kolkata to Bankura', 
                 'Asansol (West Bengal) to Kolkata', 'Midnapore to Kolkata', 'Kolkata to Asansol (West Bengal)', 
                 'Kolkata to Siliguri', 'Kolkata to Nimtouri', 'Siliguri to Kolkata', 'Kolkata to Contai (Kanthi)', 
                 'Digha to Durgapur (West Bengal)', 'Kolkata to Midnapore', 'Kolkata to Nandakumar (west bengal)', 
                 'Kolkata to Burdwan'],
        'West Bengal': ['Kolkata to Digha', 'Digha to Kolkata', 'Burdwan to Kolkata', 'Durgapur (West Bengal) to Kolkata', 
                 'Haldia to Kolkata', 'Asansol (West Bengal) to Kolkata', 'Kolkata to Durgapur (West Bengal)', 
                 'Kolkata to Burdwan', 'Midnapore to Kolkata', 'Kolkata to Nimtouri', 'Nimtouri to Kolkata', 
                 'Kolkata to Arambagh (West Bengal)', 'Arambagh (West Bengal) to Kolkata', 'Kolkata to Asansol (West Bengal)', 
                 'Siliguri to Kolkata', 'Kolkata to Siliguri', 'Kolkata to Contai (Kanthi)', 'Contai (Kanthi) to Kolkata', 
                 'Kolkata to Nandakumar (west bengal)', 'Nandakumar (west bengal) to Kolkata'],
        'Chandigarh (CTU)': ['Delhi to Chandigarh', 'Chandigarh to Delhi', 'Chandigarh to Shimla', 'Shimla to Chandigarh', 
                 'Chandigarh to Manali', 'Manali to Chandigarh', 'Chandigarh to Dehradun', 'Dehradun to Chandigarh', 
                 'Chandigarh to Jaipur (Rajasthan)', 'Jaipur (Rajasthan) to Chandigarh', 'Chandigarh to Haridwar', 
                 'Haridwar to Chandigarh', 'Chandigarh to Jalandhar', 'Jalandhar to Chandigarh', 'Chandigarh to Katra', 
                 'Katra to Chandigarh', 'Chandigarh to Pathankot', 'Pathankot to Chandigarh', 'Chandigarh to Kullu', 
                 'Kullu to Chandigarh', 'Chandigarh to Dharamshala (Himachal Pradesh)', 'Dharamshala (Himachal Pradesh) to Chandigarh', 
                 'Chandigarh to Ludhiana', 'Ludhiana to Chandigarh', 'Chandigarh to Amritsar', 'Amritsar to Chandigarh', 
                 'Chandigarh to Jammu', 'Jammu to Chandigarh', 'Chandigarh to Gurdaspur', 'Gurdaspur to Chandigarh', 
                 'Chandigarh to Kangra', 'Kangra to Chandigarh', 'Chandigarh to Ambala', 'Ambala to Chandigarh'],
        'Assam (ASTC)': ['Guwahati to Jorhat', 'Jorhat to Guwahati', 'Guwahati to Sivasagar', 'Guwahati to Tezpur', 
                 'Guwahati to Tinsukia', 'Tezpur to Guwahati', 'Guwahati to Dibrugarh', 'Sivasagar to Guwahati', 
                 'Guwahati to Nagaon', 'Tinsukia to Guwahati', 'Guwahati to Silchar', 'Guwahati to Bongaigaon', 
                 'Guwahati to Bongaigaon', 'Guwahati to Nalbari', 'Guwahati to Barpeta', 'Guwahati to Lakhimpur', 
                 'Guwahati to Nalbari', 'Nagaon to Guwahati', 'Bongaigaon to Guwahati', 'Silchar to Guwahati', 
                 'Lakhimpur to Guwahati', 'Barpeta to Guwahati', 'Nalbari to Guwahati', 'Dibrugarh to Guwahati'],
        'Kadamba (KTCL)': ['Panjim to Margao', 'Margao to Panjim', 'Margao to Vasco', 'Panjim to Vasco', 'Vasco to Panjim', 
                 'Vasco to Margao', 'Mapusa to Panjim', 'Panjim to Mapusa', 'Panjim to Calangute', 'Calangute to Panjim', 
                 'Panjim to Canacona', 'Canacona to Panjim', 'Mapusa to Calangute', 'Calangute to Mapusa', 
                 'Mapusa to Margao', 'Margao to Mapusa', 'Panjim to Ponda', 'Ponda to Panjim', 'Mapusa to Vasco', 
                 'Vasco to Mapusa']
    }

    route = route_dict.get(state_transport_corp, [])

    bus_route = st.selectbox('Select the route:', route)

    bus_type = st.selectbox('Select the bus type:', ['Sleeper', 'Seater'])

    air_con = st.selectbox('Select A/C or Non A/C:', ['A/C', 'Non A/C'])

    ratings = st.selectbox('Select the ratings:', ['4 to 5', '3 to 4', '2 to 3', '1 to 2', '0 to 1', 'unrated'])

    starting_time = st.selectbox('Select the starting time:', ['00:00 to 06:00', '06:00 to 12:00', '12:00 to 18:00', '18:00 to 24:00'])

    price_option = ['upto ₹200', 'upto ₹400', 'upto ₹600', 'upto ₹800', 'upto ₹1000', '₹1000+']
    price = st.select_slider('Select the bus fare:', price_option)

    click_button = st.button('Search')

if click_button:
    # Build the query
    bustype_query = {
        ('Sleeper', 'A/C'): """bustype LIKE '%Sleeper%' AND (bustype LIKE '%A/C%' OR bustype LIKE 'A/C%')""",
        ('Seater', 'A/C'): """bustype LIKE '%Seater%' AND (bustype LIKE '%A/C%' OR bustype LIKE 'A/C%') AND bustype LIKE '%MULTI AXLE'""",
        ('Sleeper', 'Non A/C'): """bustype LIKE '%Sleeper%' AND (bustype LIKE '%Non%' OR bustype LIKE 'Non%' OR bustype LIKE 'NON%')""",
        ('Seater', 'Non A/C'): """bustype LIKE '%Seater%' AND (bustype LIKE '%Non%' OR bustype LIKE 'Non%' OR bustype LIKE 'NON%')"""
    }.get((bus_type, air_con), '')

    rating_query = {
        '4 to 5': "star_rating >= 4 AND star_rating <= 5",
        '3 to 4': "star_rating >= 3 AND star_rating <= 4",
        '2 to 3': "star_rating >= 2 AND star_rating <= 3",
        '1 to 2': "star_rating >= 1 AND star_rating <= 2",
        '0 to 1': "star_rating > 0 AND star_rating <= 1",
        'unrated': "star_rating = 0"
    }.get(ratings, '')

    time_query = {
        '00:00 to 06:00': "departing_time >= '00:00:00' AND departing_time <= '06:00:00'",
        '06:00 to 12:00': "departing_time >= '06:00:00' AND departing_time <= '12:00:00'",
        '12:00 to 18:00': "departing_time >= '12:00:00' AND departing_time <= '18:00:00'",
        '18:00 to 24:00': "departing_time >= '18:00:00' AND departing_time <= '23:59:59'"
    }.get(starting_time, '')

    price_query = {
        'upto ₹200': "price <= 200",
        'upto ₹400': "price <= 400",
        'upto ₹600': "price <= 600",
        'upto ₹800': "price <= 800",
        'upto ₹1000': "price <= 1000",
        '₹1000+': "price > 1000"
    }.get(price, '')

    filters = []
    if bustype_query:
        filters.append(bustype_query)
    if rating_query:
        filters.append(rating_query)
    if time_query:
        filters.append(time_query)
    if price_query:
        filters.append(price_query)

    query_conditions = ' AND '.join(filters) if filters else '1'

    query = f"""SELECT * FROM All_bus_data WHERE route_name LIKE '%{bus_route}%' AND {query_conditions}"""

    rows, column_names = fetch_data(query)

    # Convert to DataFrame and display
    df = pd.DataFrame(rows, columns=column_names)
    st.write(df)


# In[ ]:




