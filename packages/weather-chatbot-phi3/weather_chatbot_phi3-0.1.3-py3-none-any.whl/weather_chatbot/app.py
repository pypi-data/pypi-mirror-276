import os
import gradio as gr
from llama_cpp import Llama
import requests
import huggingface_hub

# Download model from Hugging Face if not already present
model_path = "./model/phi-3-gguf/Phi-3-mini-4k-instruct-q4.gguf"

# Initialize the Llama model
llm = Llama(
    model_path=model_path,
    n_ctx=4096,
    n_threads=8,
    n_gpu_layers=0,
)

# OpenWeatherMap API settings
api_key = '337586e7326dcb828d7a386379093040'

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description']
        temp = data['main']['temp']
        wind_speed = data['main']['speed']
        return f"Weather: {weather_description}, Temperature: {temp}°C, Wind Speed: {wind_speed} m/s"
    else:
        return "Could not fetch weather data. Please try again."

def respond(message, history):
    try:
        # Check if the message contains a weather query
        if 'weather' in message.lower():
            city = message.split()[-1]  # Assuming the city is the last word in the message
            weather_info = get_weather(city)
            history.append((message, weather_info))
            return weather_info, history

        # Append the new message to the history
        history.append((message, ""))
        
        # Create the prompt based on the history
        prompt = "\n".join([f"{'User' if i % 2 == 0 else 'Assistant'}: {m[0]}" for i, m in enumerate(history)]) + "\nAssistant:"

        # Generate response
        output = llm(prompt, max_tokens=256, temperature=1.0, top_p=0.9, echo=False)
        response = output['choices'][0]['text'].strip()

        # Update history with the assistant's response
        history[-1] = (history[-1][0], response)

        return response, history
    except Exception as e:
        return f"An error occurred: {e}", history

# Define the Gradio interface
with gr.Blocks(css="style.css") as demo:
    gr.Markdown(
        """
        # Weather Chatbot
        Get real-time weather forecasts or chat with our assistant. Type your queries in natural language.
        """
    )
    with gr.Row():
        with gr.Column():
            message = gr.Textbox(label="Ask a weather question or chat with the assistant", lines=2, placeholder="Type your question here...")
            response = gr.Textbox(label="Response", lines=2)
            state = gr.State([])
            btn = gr.Button("Submit")
            btn.click(respond, [message, state], [response, state])
    
    gr.Examples(
        examples=[
            ["What's the weather in New York?"],
            ["Tell me the weather forecast for Tokyo."],
            ["What's the temperature in London?"]
        ],
        inputs=message
    )

# Launch the Gradio interface
def main():
    demo.launch(share=True, debug=True)

if __name__ == "__main__":
    main()