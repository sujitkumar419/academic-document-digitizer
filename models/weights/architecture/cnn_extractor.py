import numpy as np

def get_feature_extractor():
    # Placeholder returning a dummy layout vector generator
    return None

def extract_image_features(img_path, extractor_model):
    # Generates a clean 2048-dimensional normalized dummy array vector
    np.random.seed(42)
    mock_features = np.random.randn(2048)
    return mock_features / (np.linalg.norm(mock_features) + 1e-8)
