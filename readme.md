# About Local-LLM

This Local-LLM project will give you the ability to host your own LLM on your machine locally.

You can use it with **LM Studio** or **OpenAI** *.

For use with **OpenAI** you need edit the code and add your own OpenAI API key.

If you have questions or optimization-suggestions you can writ it down in **Issues** or **Pull request** section.

# Installation
1. Install "**conda**"
    - Windows: [Download](https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe)
    - Linux: [Download](https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh)

2. Create environment
```
conda create -n local-llm python=3.10
```

3. Enable the environment
```
conda activate local-llm
```

4. Install the **requirements**
```
pip install -r requirements.txt
```

5. Run the **app** via **streamlit**
```
streamlit run app.py
```

6. Now the streamlit server is started and the output looks like this:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.178.176:8501
```
