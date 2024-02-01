from openai import OpenAI
client = OpenAI()

inpPrompt = input("Enter your prompt: ")

response = client.images.generate(
  model="dall-e-3",
  prompt=inpPrompt,
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url1 = response.data[0].url

print(image_url)
