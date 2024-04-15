import streamlit as st
from diffusers import LCMScheduler, AutoPipelineForText2Image
import torch
import io

st.set_page_config(page_title="LangOne Artist", page_icon="🎨")


# Define the generator based on the seed value
def define_generator(seed):
    if seed == -1:  # Use random seed if -1 is provided
        generator = torch.default_generator
    else:
        generator = torch.manual_seed(seed)  # Use provided seed
    return generator


# Title
st.title("LangOne Artwork using LCM")
st.markdown(
    "Be patient, Loading for the first time will take time for downloading the files")

# Sidebar
st.sidebar.header("Parameters")
prompt = st.text_area(
    "Prompt", "Self-portrait oil painting, a beautiful cyborg with golden hair, 8k")
height = st.sidebar.number_input(
    "Height", min_value=1, value=640)
width = st.sidebar.number_input(
    "Width", min_value=1, value=480)
num_inference_steps = st.sidebar.slider(
    "Number of Inference Steps", 1, 10, 4)
guidance_scale = st.sidebar.slider("Guidance Scale", 0.0, 10.0, 0.0)
seed = st.sidebar.text_input(
    "Random Seed (-1 for default random seed)", "-1")

try:
    seed = int(seed)
except ValueError:
    st.error("Seed must be an integer.")
    st.stop()

# Initialize the diffusion pipeline
pipe = AutoPipelineForText2Image.from_pretrained(
    "Lykon/dreamshaper-7", torch_dtype=torch.float16, variant="fp16", safety_checker=None,)
pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
pipe.to("cuda")

# Load and fuse LCM LORA
pipe.load_lora_weights("latent-consistency/lcm-lora-sdv1-5")
pipe.fuse_lora()

# Generate image
if st.button("Generate Image"):
    try:
        generator = define_generator(seed)
        image = pipe(prompt=prompt,
                     num_inference_steps=num_inference_steps,
                     guidance_scale=guidance_scale,
                     height=height,
                     width=width).images[0]
        st.image(image, caption="Generated Image", use_column_width=True)

        # Allow image download
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes.seek(0)
        st.sidebar.download_button(
            label="Download Image",
            data=image_bytes,
            file_name="generated_image.png",
            mime="image/png"
        )
    except Exception as e:
        st.error(f"Error generating image: {e}")
