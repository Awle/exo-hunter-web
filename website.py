import streamlit as st
import requests
import os
import pandas as pd
from manim import *
import json
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import savgol_filter

# Configure page
st.set_page_config(layout="centered", page_title="ExoHunter", page_icon="🪐")

#Reduce all padding
padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        # padding-right: {padding}rem;
        # padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """,
            unsafe_allow_html=True)

# Set background
page_bg_img = '''
<style>
.stApp {
background-image: url("https://i.pinimg.com/originals/1e/2e/94/1e2e94461ceb179772740c2243763014.jpg");
# background-size: cover;
}
.stApp:before {
  content: "";
  position: fixed;
  top: 0; bottom: 0; left: 0; right: 0;
  background: hsla(180,0%,0%,0.65);
  pointer-events: none;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# st.markdown('<style>body{background-color: Green;}</style>',
#             unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center;color:white'>Welcome to The Exoplanet Hunter</h1>",
            unsafe_allow_html=True)

# Subtitle
st.markdown(
    "<h2 style='text-align: center;color:white'>Please upload a Light Curve below or enter a valid KepID:</h2>",
    unsafe_allow_html=True)

# Initialise values
data_input = 0
uploaded_file=None
kepid=None
df=None
list_of_values=None
final_res=None
response = None
response_df = None

# Read KepID database
keplers = pd.read_csv('data/keplerid_for_manim.csv')

# Read uploads
uploaded_file = st.file_uploader("Select a CSV file", type="csv", help="File extension must be '.csv'")
if uploaded_file is not None:
    data_input = 1
if data_input==1:
    df = pd.read_csv(uploaded_file)
    df = df.interpolate()
    list_of_values = list(df.values[:,0])
    if df is not None:
        data_input=1

kepid = st.text_input("Select a KepID",
              placeholder="Please input a KepID",
              help="Takes the form of 7 or 8 numerical digits")
if kepid != '':
    kepid = int(kepid)
    if kepid in keplers[['kepid']].values:
        data_input=2

#st.markdown((data_input, kepid))


#Prep data and dump data into a csv file for animation.py to use
if data_input!=2:
    if data_input==0:
        df = pd.read_csv('data/pos_ex.csv')
        X_imp = df.squeeze()
        X_filt = savgol_filter(X_imp, 71, 3)
    elif data_input==1:
        df.to_csv('animation_data.csv',index=False)
        X_imp = df.squeeze()
        X_filt = savgol_filter(X_imp, 71, 3)

base_url = 'https://exohunter-api-2zte5wxl7q-an.a.run.app'
curve_url = base_url + '/predictcurve'
id_url = base_url + '/predictid'
# curve_url = 'http://127.0.0.1:8000/predictcurve'
# id_url = 'http://127.0.0.1:8000/predictid'

# Output the user's data in a digestible graph
# Raw Data
if data_input != 2:
    if data_input == 1:
        st.markdown("<h3 style='text-align: center; '>Your Raw Data</h3>",
                    unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='text-align: center; '>Example Raw Data</h3>",
                    unsafe_allow_html=True)
    fig1, ax1 = plt.subplots(1, 1, figsize=(72, 16))
    sns.set(style="ticks", rc={"lines.linewidth": 7})
    sns.lineplot(x=np.arange(0, X_imp.shape[-1], 1),
                 y=X_imp,
                 ax=ax1,
                 color='orange')
    ax1.axis('off')
    st.pyplot(fig1, transparent=True)

# Filtered Data
if data_input != 2:
    if data_input:
        st.markdown("<h3 style='text-align: center; '>Your Filtered Data</h3>",
                    unsafe_allow_html=True)
    else:
        st.markdown(
            "<h3 style='text-align: center; '>Example Filtered Data</h3>",
            unsafe_allow_html=True)
    fig2, ax2 = plt.subplots(1, 1, figsize=(72, 16))
    sns.set(style="ticks", rc={"lines.linewidth": 7})
    sns.lineplot(x=np.arange(0, X_filt.shape[-1], 1),
                 y=X_filt,
                 ax=ax2,
                 color='orange')
    ax2.axis('off')
    st.pyplot(fig2, transparent=True)


# Output results
if data_input:
    st.markdown(
        "<h2 style='text-align: center;color:white '>Result:</h2>",
        unsafe_allow_html=True)
#Getting result from the API
if data_input == 1:
    with st.spinner('Running calculation...'):
        try:
            response = requests.post(curve_url, json={'instances': list_of_values})
        except:
            st.error('Error connecting to API')
elif data_input == 2:
    with st.spinner('Running calculation...'):
        try:
            response = requests.post(id_url, json={'kepid': kepid})
        except:
            st.error('Error connecting to API')

if response is not None:
    response = response.json()
    json_object = json.dumps(response, indent=4)
    # Writing to sample.json
    with open("response.json", "w") as outfile:
        outfile.write(json_object)
    st.success('Done!')
    final_res = response['prediction']
    if final_res == 'This star is LIKELY to have exoplanet(s)':
        st.markdown(
        f"<h3 style='text-align: center;color:green'>{final_res}</h3>",
        unsafe_allow_html=True)
    else:
        st.markdown(
            f"<h3 style='text-align: center;color:red'>{final_res}</h3>",
            unsafe_allow_html=True)

if data_input == 2:
    response.pop('prediction', None)
    response_df = pd.DataFrame(response)
st.dataframe(response_df)


# # FFT
# st.markdown(
#     "<h3 style='text-align: center; '>Frequency Data</h3>",
#     unsafe_allow_html=True)
# fig3, ax3 = plt.subplots(1, 1, figsize=(72, 16))
# sns.set(style="ticks", rc={"lines.linewidth": 7})
# sns.lineplot(x=np.arange(0, len(X)-1, 1), y=X[1:], ax=ax3, color='orange')
# ax3.axis('off')
# st.pyplot(fig3, transparent=True)

#url = 'https://exohunter-container-2zte5wxl7q-an.a.run.app'

# if final_res:
#     st.metric(label='Confidence level', value='60%', delta=None, delta_color="normal")


if final_res == 'This star is LIKELY to have exoplanet(s)':
    st.text(
        '''⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠁⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠙⠿⠿⠿⠻⠿⠿⠟⠿⠛⠉⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⢰⣹⡆⠀⠀⠀⠀⠀⠀⣭⣷⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠈⠉⠀⠀⠤⠄⠀⠀⠀⠉⠁⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢾⣿⣷⠀⠀⠀⠀⡠⠤⢄⠀⠀⠀⠠⣿⣿⣷⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠉⠀⠀⠀⠀⠀⢄⠀⢀⠀⠀⠀⠀⠉⠉⠁⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿

⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⣠⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣀⣀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿''')

    #kepler_name  = st.text_input(label='Awesome! What would you like to nickname your planet?', value='keplerid')
if data_input == 2:
    if final_res == 'This star is LIKELY to have exoplanet(s)':
        #Run the script to make the animation
        os.system("manim --quality l --format mp4 animation.py LoopOrbit")
        #Remove the partial animation
        os.system(
            "find media/videos/animation/480p15/partial_movie_files/LoopOrbit -name '*.mp4' -delete"
        )
        #Display the animation on streamlit
        video_file = open('media/videos/animation/480p15/LoopOrbit.mp4', 'rb')
        video_bytes = video_file.read()
    else:
        #Run the script to make the animation
        os.system(
            "manim --quality l --format mp4 animation.py NoExo"
            )
        #Remove the partial animation
        os.system(
            "find media/videos/animation/480p15/partial_movie_files/NoExo -name '*.mp4' -delete"
            )
        #Display the animation on streamlit
        video_file = open(
            'media/videos/animation/480p15/NoExo.mp4', 'rb'
            )
        video_bytes = video_file.read()


    if final_res: # Depends on data_input
        st.markdown(
            "<h1 style='text-align: center;color:white'>Animation</h1>",
            unsafe_allow_html=True)
        if (final_res == 'This star is LIKELY to have exoplanet(s)') and (
                os.path.isfile('media/videos/animation/480p15/LoopOrbit.mp4')):
            st.video(video_bytes)
            with open("media/videos/animation/480p15/LoopOrbit.mp4",
                      "rb") as file:
                btn = st.download_button(
                    label="Download video",
                    data=file,
                    file_name="video.mp4",
                    mime="video/mp4")
        elif (final_res == 'This star is likely to NOT have exoplanet') and (os.path.isfile('media/videos/animation/480p15/NoExo.mp4')):
            st.video(video_bytes)
            with open("media/videos/animation/480p15/NoExo.mp4",
                      "rb") as file:
                btn = st.download_button(label="Download video",
                                         data=file,
                                         file_name="video.mp4",
                                         mime="video/mp4")
