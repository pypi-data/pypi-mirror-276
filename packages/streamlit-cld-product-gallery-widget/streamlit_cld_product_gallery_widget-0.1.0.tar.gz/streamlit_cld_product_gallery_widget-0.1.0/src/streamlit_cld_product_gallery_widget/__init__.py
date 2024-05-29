from pathlib import Path
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components

# Tell streamlit that there is a component called streamlit_cld_product_gallery_widget,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
	"streamlit_cld_product_gallery_widget", path=str(frontend_dir)
)

# Create the python function that will be called
def cld_product_gallery_widget(
        cloudName: str,
        mediaAssets:list,
        placeholderImage:bool=True, #start with low res placeholder image
        sortProps:dict = { 'source': "public_id", 'direction': "asc" }, #instruction on sorting
        viewportBreakpoints:list = [], #breakpoint information for generating the gallery view
        aspectRatio:str = 'square',
        imageBreakpoint:int = 250, #default size for image break-points
        videoBreakpoint:int = 250, #default size for video break-points
        preload:list = [], #load only the first image
        transition:str = 'slide', #transition style to use for display
        zoom:bool = True, #enable the zoom        
        key: Optional[str] = None,
):
    """
    Call for loading the Product Gallery Widget 
    """
    component_value = _component_func(
        cloudName=cloudName,
        mediaAssets=mediaAssets,
        placeholderImage=placeholderImage,
        sortProps=sortProps,
        viewportBreakpoints=viewportBreakpoints,
        aspectRatio=aspectRatio,
        imageBreakpoint=imageBreakpoint,
        videoBreakpoint=videoBreakpoint,
        preload=preload,
        transition=transition,
        zoom=zoom,
        key=key,
    )

    return component_value


def main():
    st.write("## Sample Product Gallery Widget")
    value = cld_product_gallery_widget(
        cloudName='demo',
        mediaAssets=[{'tag':'logo'}],
        zoom=True
    )    


if __name__ == "__main__":
    main()
