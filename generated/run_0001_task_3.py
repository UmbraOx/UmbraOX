def get_supported_features():
    """
    Retrieve a list of all features currently supported by the system.

    Returns:
        List[str]: A list containing the names of all supported features.
    """
    # Simulated list of supported features
    return [
        "Feature A",
        "Feature B",
        "Feature C",
        "Feature D"
    ]

def main():
    """
    Main function to display the supported features.
    """
    try:
        features = get_supported_features()
        if not features:
            print("No features are currently supported by the system.")
        else:
            print("Features supported by the system:")
            for feature in features:
                print(f"- {feature}")
    except Exception as e:
        print(f"An error occurred while retrieving supported features: {e}")

if __name__ == "__main__":
    main()
