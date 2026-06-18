import gradio as gr

def configure_dashboard():
    """
    Configures a simple Gradio dashboard application to run on port 7860.
    
    This function sets up a basic interface with a text input and output,
    demonstrating how to launch the application on a specific port.
    """
    try:
        # Define a simple function that echoes the input
        def echo_text(input_text):
            return input_text
        
        # Create a Gradio interface
        iface = gr.Interface(
            fn=echo_text, 
            inputs="text", 
            outputs="text",
            title="Simple Echo Dashboard"
        )
        
        # Launch the interface on port 7860
        iface.launch(server_name="0.0.0.0", server_port=7860)
    
    except Exception as e:
        print(f"An error occurred while configuring the dashboard: {e}")

if __name__ == "__main__":
    configure_dashboard()
