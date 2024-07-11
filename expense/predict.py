import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from .models import Expense

class ExpensePredictor:
    def __init__(self):
        # Initialize your machine learning model here
        self.model = self._build_model()

    def _build_model(self):
        # Example: Building a simple Linear Regression model pipeline
        model_pipeline = Pipeline([
            ('scaler', StandardScaler()),  # Example: Scaling features
            ('regressor', LinearRegression())  # Example: Linear Regression model
        ])
        return model_pipeline

    def _prepare_time_series_data(self, user_id):
        # Example function to prepare time series data for prediction
        try:
            expenses = Expense.objects.filter(user_id=user_id).order_by('date')
            df = pd.DataFrame(list(expenses.values('date', 'amount')))
            
            # Creating time-based features
            df['date'] = pd.to_datetime(df['date'], errors='coerce')

            df['month'] = df['date'].dt.month
            df['year'] = df['date'].dt.year
            # df['day_of_week'] = df['date'].dt.dayofweek
            # df['day_of_month'] = df['date'].dt.day
            
            # Assuming we're using amount as the target and time-based features as predictors
            X = df[['month', 'year']]
            y = df['amount']
            return X, y
        except Exception as e:
            print(e)

    def train(self, user_id):
        # Training the model on user's expense data
        X, y = self._prepare_time_series_data(user_id)
        self.model.fit(X, y)

    def predict_future_expenses(self, user_id, n_periods=12):
        # Predicting future expenses
        X, _ = self._prepare_time_series_data(user_id)
        
        # Generating future time features
        last_date = Expense.objects.filter(user_id=user_id).latest('date').date
        future_dates = [last_date + pd.DateOffset(months=i) for i in range(1, n_periods+1)]
        future_df = pd.DataFrame(future_dates, columns=['date'])
        future_df['month'] = future_df['date'].dt.month
        future_df['year'] = future_df['date'].dt.year
        # future_df['day_of_week'] = future_df['date'].dt.dayofweek
        # future_df['day'] = future_df['date'].dt.day
        
        # Predicting future expenses
        future_X = future_df[['month', 'year']]
        future_predictions = self.model.predict(future_X)
        future_df['predicted_amount'] = future_predictions
        
        return future_df[['date', 'predicted_amount']].to_dict(orient='records')
