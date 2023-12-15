import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load the Phi 2 model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    "microsoft/phi-2",
    trust_remote_code=True
)

model = AutoModelForCausalLM.from_pretrained(
    "microsoft/phi-2",
    device_map="auto",
    trust_remote_code=True
)

# Streamlit UI
st.title("Microsoft Phi 2 Streamlit App")

# User input prompt
prompt = st.text_area("Enter your prompt:", """Write a story about Nasa""")

# Generate output based on user input
if st.button("Generate Output"):
    with torch.no_grad():
        token_ids = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
        output_ids = model.generate(
            token_ids.to(model.device),
            max_new_tokens=512,
            do_sample=True,
            temperature=0.3
        )

    output = tokenizer.decode(output_ids[0][token_ids.size(1):])
    st.text("Generated Output:")
    st.write(output)
