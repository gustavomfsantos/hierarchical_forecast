## Nixtla Hierarchical Forecasting

# Overview
Nixtla is a Python package that introduces a novel approach to time series forecasting called Hierarchical Forecasting. This approach involves predicting time series at multiple aggregation levels and subsequently reconciling these forecasts to generate accurate predictions at higher levels.

All credits for the package is due https://github.com/Nixtla/hierarchicalforecast

I only used with another structure and for another dataset

# Features
- Hierarchical Forecasting: Predict time series at various aggregation levels.
- Reconciliation: Merge forecasts at different levels to achieve a coherent and accurate prediction for the entire time series.

Getting Started with installation, please check the Nixtla instructions: https://github.com/Nixtla/hierarchicalforecast

# How it Works
Hierarchical Forecasting gained prominence following the research by Hyndman (2017). Nixtla adopts this approach, predicting time series at different aggregation levels. The forecasts at lower levels are used to assist in predicting higher-level aggregations, resulting in a more accurate and comprehensive forecast.


License
This project is licensed under the MIT License - see the LICENSE file for details 
https://github.com/Nixtla/hierarchicalforecast.

Acknowledgments
Hyndman, R. J. (2017). Forecasting: principles and practice. Monash University.

Nixtla Team - https://github.com/Nixtla/hierarchicalforecast

If you encounter any issues or have questions, feel free to open an issue or reach out to the maintainers.

