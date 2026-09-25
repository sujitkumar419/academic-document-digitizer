import os
import numpy as np
from models.weights.architecture.cnn_extractor import get_feature_extractor, extract_image_features
from pipeline.transform import normalize_metadata_features, merge_vision_and_metadata
from models.weights.architecture.ml_classifiers import load_classifier
from models.weights.architecture.dl_perceptron import LayerDense, ActivationSigmoid

class MasterInferenceEvaluator:
    def __init__(self):
        self.extractor = get_feature_extractor()
        
        # Initialize custom mathematical neural network layers (Phase 1 & 2 logic)
        self.dense1 = LayerDense(2052, 16)
        self.activation1 = ActivationSigmoid()
        self.dense2 = LayerDense(16, 1)
        self.activation2 = ActivationSigmoid()
        
    def execute_complete_evaluation(self, img_path, word_count, formula_density, has_diagrams, image_brightness):
        # 1. Pipeline Stage 1: Dynamic Computer Vision Feature Extraction
        vision_features = extract_image_features(img_path, self.extractor)
        
        # 2. Pipeline Stage 2: NumPy Array Vector Scale Standardizations
        metadata_features = normalize_metadata_features(word_count, formula_density, has_diagrams, image_brightness)
        
        # 3. Pipeline Stage 3: Merge Multimodal Vectors
        combined_vector = merge_vision_and_metadata(vision_features, metadata_features)
        
        # 4. Pipeline Stage 4: Run Deep Numerical Perceptron Graph
        self.dense1.forward(combined_vector)
        self.activation1.forward(self.dense1.output)
        self.dense2.forward(self.activation1.output)
        self.activation2.forward(self.dense2.output)
        
        final_probability = self.activation2.output
        is_approved = 1 if final_probability > 0.5 else 0
        
        return {
            'approval_probability': float(final_probability),
            'status_approved': is_approved,
            'feature_dimensions': combined_vector.shape
        }
