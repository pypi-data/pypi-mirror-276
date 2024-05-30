from app.postgres.functions import insert_csv_data_to_postgres, fetch_data
from app.general_tools.logger import logger
from app.preprocessing.preprocess import Preprocessor
from app.recommendation.recommendation import ContentRecommender
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.postgres.table_class import Base
import uvicorn
from contextlib import asynccontextmanager

# Global engine and session maker
engine = create_engine('postgresql://gpanagou:my_secret_password@db/htb')
Session = sessionmaker(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):

    Base.metadata.create_all(engine)
    session = Session()
    csv_files_map = [
        ('data/machines.csv', 'machines'),
        ('data/machine_ratings.csv', 'machine_ratings'),
        ('data/content_owns.csv', 'content_owns')
    ]
    insert_csv_data_to_postgres(csv_files_map)
    session.close()
    yield

# Create an instance of FastAPI
app = FastAPI(lifespan=lifespan)

# Define endpoint for serving user progress
@app.get("/progress/{user_id}")
async def get_user_progress(user_id: str):
    # Dummy progress for demonstration
    progress = {"user_id": user_id, "progress": 75}
    return progress

# Define endpoint for serving recommendations
@app.get("/recommendations/{user_id}")
async def get_recommendations(user_id: str):
    try:
        session = Session()

        # Fetch data and prepare it for processing
        df = fetch_data(session)
        cols = [
            'user_uuid', 'content_name', 'avg_rating', 'points', 'user_points',
            'root_points', 'total_points', 'own_type', 'os', 'variety', 'difficulty', 'description'
        ]
        numerical_cols = [
            'user_points', 'root_points', 'total_points', 'points', 'own_type', 'os',
            'avg_rating', 'variety', 'difficulty'
        ]
        
        # Initialize the preprocessor and preprocess data
        preprocessor = Preprocessor(cols, numerical_cols)
        df_selected = df[cols]
        df_encoded = preprocessor.map_categorical(df_selected)
        df_encoded = preprocessor.normalize_numerical_features(df_encoded)
        train_df, test_df, val_df = preprocessor.train_test_val_split(df_encoded)
        # Initialize the recommender system with the preprocessed data
        recommender = ContentRecommender(train_df)
        
        # Get recommendations for the user
        recommendations = recommender.recommend_content(user_id)
        return {"user_id": user_id, "recommendations": list(recommendations)}
    
    except Exception as e:
        logger.error(f"An error occurred during recommendation: {str(e)}")
        return {"error": str(e)}
    
    finally:
        session.close()


if __name__ == "__main__":
    # Run the FastAPI application
    uvicorn.run(app, host="127.0.0.1", port=8000)