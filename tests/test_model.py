from backend.llm.model_loader import model, tokenizer

print("Model Loaded Successfully")

prompt = "Explain OAuth2 authentication in one paragraph."

inputs = tokenizer(
    prompt,
    return_tensors="pt"
).to(model.device)

outputs = model.generate(
    **inputs,
    max_new_tokens=100
)

response = tokenizer.decode(
    outputs[0],
    skip_special_tokens=True
)

print("\nRESPONSE:\n")
print(response)