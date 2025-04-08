import os
from kaggle.api.kaggle_api_extended import KaggleApi

def download_kaggle_dataset(dataset, output_dir):
    api = KaggleApi()
    api.authenticate()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Downloading dataset: {dataset}...")
    api.dataset_download_files(dataset, path=output_dir, unzip=True)
    print(f"Dataset downloaded and saved in: {output_dir}")

if __name__ == "__main__":
    dataset = "andradaolteanu/gtzan-dataset-music-genre-classification"
    output_directory = "music_dataset"

    download_kaggle_dataset(dataset, output_directory)
