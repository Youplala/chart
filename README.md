[![Downloads](https://static.pepy.tech/badge/chartgpt)](https://pepy.tech/project/chartgpt)

![ChartGPT Logo](docs/assets/chartgpt_logo.svg)

---

ChartGPT is a lightweight and user-friendly tool designed to assist you in visualizing your Pandas dataframes. Whether you are working in a Jupyter notebook or developing a Dash application, ChartGPT makes it effortless to generate stunning charts and plots. 📈

## Features 🌟

- Intuitive integration with Pandas dataframes 🐼
- Supports both Jupyter notebooks and Dash applications 📓🚀
- Simple installation and setup ⚙️

## Installation ⬇️

You can install ChartGPT using pip:

```bash
pip install chartgpt
```

## Example Usage 🎉

### Jupyter Notebook 📔

```python
import chartgpt as cg

df = pd.read_csv('data.csv')
chart = cg.Chart(df, api_key="YOUR_API_KEY")
chart.plot("Pop vs. State")
```

![ChartGPT in a Jupyter notebook](docs/assets/chart.png)

Generated graph after inputting 'Pop vs. State'

### Dash App 🚀

![ChartGPT in a Dash app](docs/assets/dash.png)

## Documentation 📚

For detailed information on how to use ChartGPT, please refer to the [documentation](https://chatgpt.github.io/chart/).

## License 📜

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
