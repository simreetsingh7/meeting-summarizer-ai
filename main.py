from openai import OpenAI

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)

completion = client.chat.completions.create(
  model="nvidia/nemotron-3-super-120b-a12b",
  messages=[
      {"role": "system", "content": "You are a Micro-SaaS expert. Give 3 concise ideas."}, 
      {"role": "user", "content": "Give me 3 Micro-SaaS ideas I can build in 24 hours with free tools. Keep each idea under 100 words so the full list fits in one response."}
  ],
  max_tokens=800, # Lowered to ensure it finishes
  stream=False
)

print(completion.choices[0].message.content)   