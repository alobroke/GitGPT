import torch

from backend.llm.model_loader import (
    model,
    tokenizer
)


class Generator:

    def generate(
        self,
        prompt,
        max_new_tokens=300
    ):

        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=4096
        ).to(model.device)

        with torch.no_grad():

            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                temperature=0.0,
                top_p=1.0,
                repetition_penalty=1.1,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id
            )

        generated_tokens = outputs[0][
            inputs["input_ids"].shape[1]:
        ]

        response = tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True
        )

        return response.strip()