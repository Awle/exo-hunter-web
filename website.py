import streamlit as st
import requests
import os
import pandas as pd
from manim import *

import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import savgol_filter
from pyts.preprocessing import InterpolationImputer

# Configure page
st.set_page_config(layout="wide", page_title="ExoHunter", page_icon="🪐")

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
body {
background-image: url("https://www.almanac.com/sites/default/files/styles/landscape/public/image_nodes/sunflower-1627193_1920.jpg?itok=dhvHrrYK");
background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center; color: white;'>Welcome to The Exoplanet Hunter</h1>",
            unsafe_allow_html=True)

# Subtitle
st.markdown(
    "<h2 style='text-align: center; color: white;'>Please upload Lightcurve below:</h2>",
    unsafe_allow_html=True)

# Initialise values
data_input = False
df=None
list_of_values=None
final_res=None

# Read uploads
uploaded_files = st.file_uploader('Select a CSV file', accept_multiple_files=True)
for uploaded_file in uploaded_files:
    df = pd.read_csv(uploaded_file)
    df = df.interpolate()
    list_of_values = list(df.values[:,0]) #list(np.nan_to_num(df.values[:,0], copy=False, nan=-666))
    if df is not None:
        data_input=True

#Prep data and dump data into a csv file for animation.py to use
if data_input:
    df.to_csv('animation_data.csv',index=False)
else:
    df = pd.read_csv('data/pos_ex.csv')

X_imp = df.interpolate().squeeze()
X_filt = savgol_filter(X_imp, 71, 3)
# data_fft = pd.DataFrame(np.abs(np.fft.fft(X_filt, axis=1)))
# data_fft = data_fft.iloc[:,:(len(data_fft) // 2)]
# X = data_fft.iloc[60]

# Output the user's data in a digestible graph
if data_input:
    st.markdown(
        "<h2 style='text-align: left; color: white;'>Your Data:</h2>",
        unsafe_allow_html=True)

# Raw Data
if data_input:
    st.markdown(
        "<h3 style='text-align: center; color: white;'>Raw Data</h3>",
        unsafe_allow_html=True)
else:
    st.markdown("<h3 style='text-align: center; color: white;'>Example Raw Data</h3>",
                unsafe_allow_html=True)
fig1, ax1 = plt.subplots(1, 1, figsize=(72, 16))
sns.set(style="ticks", rc={"lines.linewidth": 7})
sns.lineplot(x=np.arange(0, X_imp.shape[-1], 1), y=X_imp, ax=ax1, color='orange')
ax1.axis('off')
st.pyplot(fig1, transparent=True)

# Filtered Data
if data_input:
    st.markdown(
        "<h3 style='text-align: center; color: white;'>Filtered Data</h3>",
        unsafe_allow_html=True)
else:
    st.markdown(
        "<h3 style='text-align: center; color: white;'>Example Filtered Data</h3>",
        unsafe_allow_html=True)
fig2, ax2 = plt.subplots(1, 1, figsize=(72, 16))
sns.set(style="ticks", rc={"lines.linewidth": 7})
sns.lineplot(x=np.arange(0, X_filt.shape[-1], 1), y=X_filt, ax=ax2, color='orange')
ax2.axis('off')
st.pyplot(fig2, transparent=True)

# # FFT
# st.markdown(
#     "<h3 style='text-align: center; color: white;'>Frequency Data</h3>",
#     unsafe_allow_html=True)
# fig3, ax3 = plt.subplots(1, 1, figsize=(72, 16))
# sns.set(style="ticks", rc={"lines.linewidth": 7})
# sns.lineplot(x=np.arange(0, len(X)-1, 1), y=X[1:], ax=ax3, color='orange')
# ax3.axis('off')
# st.pyplot(fig3, transparent=True)

#url = 'https://exohunter-container-2zte5wxl7q-an.a.run.app'
url = 'http://127.0.0.1:8000/predictcurve'

# Output results
if data_input:
    st.subheader('Result:')
#Getting result from the API
if list_of_values:
    with st.spinner('Running calculation...'):
        response = requests.post(url,json={'instances': list_of_values})
        response = response.json()
    st.success('Done!')
    final_res = response['prediction']
    final_res




if final_res == 'This star is LIKELY to have exoplanet(s)':
    st.balloons()
    st.text(
        '''⣿⣿⣿⣿⣿⡏⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿
⣿⣿⣿⣿⣿⣿⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠁⠀⣿
⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠙⠿⠿⠿⠻⠿⠿⠟⠿⠛⠉⠀⠀⠀⠀⠀⣸⣿
⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣴⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⢰⣹⡆⠀⠀⠀⠀⠀⠀⣭⣷⠀⠀⠀⠸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠈⠉⠀⠀⠤⠄⠀⠀⠀⠉⠁⠀⠀⠀⠀⢿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢾⣿⣷⠀⠀⠀⠀⡠⠤⢄⠀⠀⠀⠠⣿⣿⣷⠀⢸⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡀⠉⠀⠀⠀⠀⠀⢄⠀⢀⠀⠀⠀⠀⠉⠉⠁⠀⠀⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿

⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⣠⣤⣶⣶
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢰⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣀⣀⣾⣿⣿⣿⣿'''
    )

    kepler_name  = st.text_input(label='Awesome! What would you like to nickname your planet?', value='keplerid')

    #Run the script to make the animation
    os.system("manim --quality l --format mp4 animation.py FollowingGraphCamera")
    #Remove the partial animation
    os.system("find media/videos/animation/480p15/partial_movie_files/FollowingGraphCamera -name '*.mp4' -delete")
    #Display the animation on streamlit
    video_file = open('media/videos/animation/480p15/FollowingGraphCamera.mp4', 'rb')
    video_bytes = video_file.read()

if data_input:
    st.title('Animation')
    if os.path.isfile('media/videos/animation/480p15/FollowingGraphCamera.mp4'):
        st.video(video_bytes)
        with open("media/videos/animation/480p15/FollowingGraphCamera.mp4", "rb") as file:
            btn = st.download_button(
                label="Download video",
                data=file,
                file_name="video.mp4",
                mime="video/mp4")
    else:
        st.write('Sorry, no animation for you')
