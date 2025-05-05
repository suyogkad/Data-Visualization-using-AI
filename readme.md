# DataVizAI Project

## Prerequisites

Before getting started, make sure you have the following tools installed:

- **Anaconda** or **Miniconda**
- **PyCharm** (or another Python IDE of your choice)

## Setup Instructions

1. **Install Anaconda/Miniconda**
   - Download the installer from the official [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) website.
   - Follow the installation prompts for your operating system.

2. **Install PyCharm**
   - Download and install PyCharm from the official [JetBrains website](https://www.jetbrains.com/pycharm/download/).

3. **Create and Activate Virtual Environment**

   Open a terminal (or Anaconda Prompt) and run:

   ```bash
   conda create -n datavizai python=3.9
   conda activate datavizai
   ```

4. **Install Dependencies**

   Go to the project folder. With the datavizai environment active, install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

5. **Running the Project**

   From within the project directory, simply run:

   ```bash
   python run.py
   ```
   
    This will start the DataVizAI application.


6. **Accessing the Application**

   Once the server is running, open your web browser and navigate to:

   ```bash
   http://127.0.0.1:5000/
   ```

