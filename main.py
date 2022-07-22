from colorthief import ColorThief
import io
import colorsys
import streamlit as st
from urllib.request import urlopen
from urllib.parse import urlparse

#helper function (check if input is URL or path, image)
def uri_validator(x):
    try:
        result = urlparse(x)
        return(all([result.scheme, result.netloc]))
    except AttributeError:
        return False


#main function
def extract_main_color(path, n_colors=3, rf='hex'):
    
    # checking if string is url or path or image object, to handle it accordingly
    IS_URL = uri_validator(path)
    
    # handle URL input
    if IS_URL == True:
        try:
            fd = urlopen(path)
            f = io.BytesIO(fd.read())
            image = ColorThief(f)
            # image.get_color(quality=10)
        except Exception:
            return("Failed to load image from URL, check your URL or try again.")
    
    # handle path or image input   
    else:
        try:
            image = ColorThief(path)
            # image.get_color(quality=10) 
        except FileNotFoundError:
            return('File not found')
        
    # get the dominant colors
    palette = image.get_palette(color_count=n_colors, quality=10)

    # return list of colors
    ext_colors = []
    for color in palette:
        
        if rf == 'hex' or rf== 'HEX':
            ext_colors.append(f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}")
            
        if rf == 'hsv' or rf== 'HSV':
            ext_colors.append(colorsys.rgb_to_hsv(*color))
        
        if rf == 'hsl' or rf== 'HSL':
            ext_colors.append(colorsys.rgb_to_hls(*color))

    return ext_colors



# code for streamlit to function
if __name__ == '__main__':
    
    from PIL import Image

    # SAMPLE_IMAGE_URL = 'https://images.bestsellerclothing.in/data/JJ/july-17-2021/234121301_g1.jpg?width=50&height=75&mode=fill&fill=blur&format=auto'
    SAMPLE_IMAGE_URL = 'https://lokeshdhakar.com/projects/color-thief/image-1.e59bc3bd.jpg'
    
    st.title('Extract Main Colors from Image')

    #helper function to load image for streamlit
    def load_image(image_file):
        img = Image.open(image_file)
        return img


    def image_uploader_streamlit(isUseSampleChecked):
        menu = ["Image", "URL"]
        choice = st.sidebar.selectbox("Menu",menu)
            
        if choice == "Image" and isUseSampleChecked == False:
                
                image_file = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])
                
                if image_file is not None:

                    # To See details
                    file_details = {"filename": image_file.name, "filetype":image_file.type,
                                        "filesize":image_file.size}
                    st.write(file_details)

                    # To View Uploaded Image
                    st.image(load_image(image_file),width=250)  
                    
                    return image_file
                
        if choice == "URL" and isUseSampleChecked == False:

                    st.subheader("URL")
                    url = st.text_input("Enter image URL" , placeholder="Enter image URL and click Fetch Image")
                    
                    if st.button('Fetch Image'):
                        st.write('We found this image!')
                        import requests
                        im = requests.get(url, stream=True).raw
                        st.image(load_image(im))              
                        return url
                    else:
                        st.write("Please enter a valid URL")
                        return None
                
                                    
    def show_sample_image_for_streamlit():
        isUseSampleChecked = st.sidebar.checkbox("Show Example with Sample Image")
        
        if isUseSampleChecked == True:
            import requests
            im = requests.get(SAMPLE_IMAGE_URL, stream=True).raw
            st.image(load_image(im))
            
        return isUseSampleChecked
        
    def get_n_colors_for_streamlit():
        return st.sidebar.slider("Number of Colors to extract", 4, 10, 4)

    
    import pandas as pd
    def display_results_in_streamlit(input_type):
        
        with st.spinner('Extracting colors...'):

            res = extract_main_color(input_type, n_colors=n_cols , rf='hex')
    
        st.success('Done!')
        
        st.write("Extracted Colours : ")
        df = pd.DataFrame(res, columns=['Color'])
        st.table(df.style.applymap(lambda x: f"background-color: {x}; color : white;"))
        
        
    # calling functions
    isSampleTrue = show_sample_image_for_streamlit()
    imdata = image_uploader_streamlit(isSampleTrue)
    n_cols = get_n_colors_for_streamlit()
    
    
    
        
    # calling main functions for streamlit according to inputs

    if imdata != None:
        display_results_in_streamlit(imdata)
        
    if isSampleTrue == True:
        display_results_in_streamlit(SAMPLE_IMAGE_URL)
