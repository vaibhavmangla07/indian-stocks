import os
import sys
from dataclasses import dataclass

from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class ModelTrainerConfig:
    """Configuration paths for trained model artifacts."""
    trained_model_file_path: str = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    """
    Trains and evaluates multiple regression models for stock price prediction.
    
    This component:
    - Trains 6 different regression models (ensemble, tree-based, linear, boosting)
    - Evaluates each model using R² score on test data
    - Selects the best performing model
    - Validates minimum quality threshold (R² > 0.6)
    - Saves the best model for inference
    """
    
    # Minimum acceptable model performance (R² score)
    MIN_MODEL_SCORE = 0.6
    
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()


    def initiate_model_trainer(self, train_array, test_array) -> float:
        """
        Execute the model training and selection pipeline.
        
        Steps:
        1. Separate features (X) and target (y) from train/test arrays
        2. Train 6 different regression models
        3. Evaluate each model on test data using R² score
        4. Select model with highest R² score
        5. Validate quality threshold (R² > 0.6)
        6. Save best model for inference
        
        Args:
            train_array: Training data as numpy array (features + target in last column)
            test_array: Test data as numpy array (features + target in last column)
            
        Returns:
            R² score of best model on test data
            
        Raises:
            CustomException: If best model score falls below minimum threshold
        """
        logging.info("Starting model training process")
        try:
            # Extract features and target from arrays
            logging.info("Separating features and target from train/test data")
            X_train = train_array[:, :-1]  # All columns except last
            y_train = train_array[:, -1]   # Last column (target)
            X_test = test_array[:, :-1]
            y_test = test_array[:, -1]
            
            logging.info(f"Training data shape: {X_train.shape}, Test data shape: {X_test.shape}")

            # Define 6 candidate regression models
            models = {
                "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
                "Decision Tree": DecisionTreeRegressor(random_state=42),
                "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, random_state=42),
                "Linear Regression": LinearRegression(),
                "XGBoost": XGBRegressor(n_estimators=100, random_state=42),
                "AdaBoost": AdaBoostRegressor(n_estimators=100, random_state=42),
            }
            
            logging.info(f"Training {len(models)} candidate models for stock prediction...")
            
            # Train and evaluate each model
            model_report = {}
            for model_name, model in models.items():
                # Train model
                model.fit(X_train, y_train)
                
                # Predict on test set
                y_pred = model.predict(X_test)
                
                # Evaluate using R² score
                test_score = r2_score(y_test, y_pred)
                model_report[model_name] = test_score
                
                logging.info(f"{model_name:20s} - R² Score: {test_score:.4f}")

            # Find best model by highest R² score
            best_model_name = max(model_report, key=model_report.get)
            best_model_score = model_report[best_model_name]
            best_model = models[best_model_name]
            
            logging.info(f"\nBest model: {best_model_name} with R² = {best_model_score:.4f}")

            # Validate model meets minimum quality threshold
            if best_model_score < self.MIN_MODEL_SCORE:
                raise CustomException(
                    f"Best model ({best_model_name}) has R² score {best_model_score:.4f} "
                    f"below minimum threshold {self.MIN_MODEL_SCORE}"
                )

            # Save best model for inference
            logging.info(f"Saving best model to {self.model_trainer_config.trained_model_file_path}")
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
            
            logging.info(f"Model training completed successfully")
            return best_model_score

        except Exception as e:
            raise CustomException(e, sys)
