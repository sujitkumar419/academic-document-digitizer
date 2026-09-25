import numpy as np

def normalize_metadata_features(word_count, formula_density, has_diagrams, image_brightness):
    features = np.array([word_count, formula_density, has_diagrams, image_brightness], dtype=float)
    
    means = np.array([425.0, 0.5, 0.5, 0.57])
    stds = np.array([216.0, 0.28, 0.5, 0.21])
    
    standardized_features = (features - means) / (stds + 1e-8)
    return standardized_features.reshape(1, -1)

def merge_vision_and_metadata(vision_features, metadata_features):
    vision_normalized = vision_features / (np.linalg.norm(vision_features) + 1e-8)
    combined_vector = np.hstack((vision_normalized.reshape(1, -1), metadata_features))
    return combined_vector