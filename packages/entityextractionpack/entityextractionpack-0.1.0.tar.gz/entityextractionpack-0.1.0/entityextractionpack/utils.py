from entityextractionpack.extraction import extract_entities, setup_environment
import os

def display_entities(prompt):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    pdf1_path = os.path.join(script_dir, "OBOL_SAMPLE.pdf")
    pdf2_path = os.path.join(script_dir, "SWB_SAMPLE.pdf")
    pages1, pages2, convo = setup_environment(pdf1_path, pdf2_path)
    all_entities = extract_entities(pages1, pages2, convo)
    
    if "pdf1" in prompt:
        print("Extracted entities from pdf1:")
        for key, value in all_entities['pdf1'].items():
            print(f"**{key}: ** {value}")
    elif "pdf2" in prompt:
        print("Extracted entities from pdf2:")
        for key, value in all_entities['pdf2'].items():
            print(f"**{key}: ** {value}")
    elif "extraction" in prompt or "result" in prompt:
        print("Extracted entities from Extraction Result:")
        # Print extracted entities from both PDFs
        for pdf, entities in all_entities.items():
            print(f"Extracted entities from {pdf}:")
            for key, value in entities.items():
                print(f"**{key}: ** {value}")
    elif "custom" in prompt:
        custom_prompt = input("Enter your custom prompt: ").lower()
        print(f"Extracted entities from custom prompt '{custom_prompt}':")
        # Add logic to extract entities based on custom prompt
        # For demonstration purposes, just printing a placeholder message
        print("Placeholder: Extracted entities based on custom prompt")
    else:
        print("Invalid input. Please enter 'pdf1', 'pdf2', 'Extraction Result', or 'Custom'.")
